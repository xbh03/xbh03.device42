#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_backup_schedules
short_description: Manage Device42 backup schedules
description:
    - Create, update, or delete Device42 backup schedules.
    - Uses C(POST /api/1.0/backup_schedules/) for create/update and
        C(DELETE /api/1.0/backup_schedules/{ID}/) for delete.
    - Endpoint uses backup schedules port C(4343) by default.
version_added: "0.2.0"
author:
    - Francesco Zoino <f.zoino@atdatenschutz.ch>
options:
    host:
        description:
            - Device42 host or IP.
        required: true
        type: str
    client_key:
        description:
            - Device42 API client key used to authenticate.
        required: false
        type: str
    client_secret_key:
        description:
            - Device42 API client secret key used to authenticate.
        required: false
        type: str
    userid:
        description:
            - Device42 username used to authenticate.
        required: false
        type: str
    password:
        description:
            - Device42 password used to authenticate.
        required: false
        type: str
    proto:
        description:
            - Protocol used to connect to Device42.
        required: false
        type: str
        default: https
        choices:
            - http
            - https
    port:
        description:
            - Device42 backup schedules endpoint port.
        required: false
        type: int
        default: 4343
    sslverify:
        description:
            - Validate SSL certificates.
        required: false
        type: bool
        default: true
    debug:
        description:
            - Enable debug behavior in helper utilities.
        required: false
        type: bool
        default: false
    state:
        description:
            - Desired state of the backup schedule.
        required: false
        type: str
        default: present
        choices:
            - present
            - absent
    name:
        description:
            - Name of backup job.
            - Required when C(state=present).
        required: false
        type: str
    method:
        description:
            - Backup method C(1=mail, 2=sftp, 3=nfs, 4=amazon s3).
            - Required when C(state=present).
        required: false
        type: str
        choices:
            - "1"
            - "2"
            - "3"
            - "4"
    schedule_time:
        description:
            - Time to perform backup in HH:MM format (00:00 to 23:59).
            - Required when C(state=present).
        required: false
        type: str
    job_id:
        description:
            - Scheduled backup ID.
            - Required when C(state=absent).
            - Optional for C(state=present) to update an existing schedule.
        required: false
        type: int
    schedule_days:
        description:
            - Comma separated days of week where Monday=0.
            - Example C(0,1,2) means Mon, Tue, Wed.
        required: false
        type: str
    force_update:
        description:
            - Force update call for existing backup schedule in C(state=present).
        required: false
        type: bool
        default: false
"""

EXAMPLES = r"""
- name: Create backup schedule
    xbh03.device42.backup_schedules.d42_api_backup_schedules:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: present
        name: test_backup
        method: "3"
        schedule_time: "03:30"
        schedule_days: 0,1,2,3,4

- name: Update backup schedule by ID
    xbh03.device42.backup_schedules.d42_api_backup_schedules:
        host: device42.example.internal
        userid: admin
        password: secret123
        state: present
        job_id: 4
        name: test_backup
        method: "4"
        schedule_time: "01:15"
        schedule_days: 0,2,4

- name: Delete backup schedule
    xbh03.device42.backup_schedules.d42_api_backup_schedules:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: absent
        job_id: 4
"""

RETURN = r"""
api_backup_schedule:
    description: Current or resulting backup schedule data when available.
    type: dict
    returned: success
response:
    description: Raw response from Device42 for create/update/delete operations.
    type: dict
    returned: when changed
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.backup_schedules.d42_backup_schedules import (
        d42_backup_schedules,
)


def _normalize_days(value):
        if value is None:
                return None
        tokens = [token.strip() for token in str(value).split(",") if token.strip() != ""]
        return ",".join(tokens)


def _extract_job_id_from_response(response):
        if not isinstance(response, dict):
                return None

        msg = response.get("msg")
        if isinstance(msg, list) and len(msg) > 1:
                try:
                        return int(msg[1])
                except (TypeError, ValueError):
                        return None

        for key in ("job_id", "id"):
                if response.get(key) is not None:
                        try:
                                return int(response.get(key))
                        except (TypeError, ValueError):
                                return None

        return None


def _get_jobs(helper):
        payload = helper.d42_get_backup_schedules()
        jobs = payload.get("jobs", [])
        return jobs if isinstance(jobs, list) else []


def _find_job(jobs, job_id=None, name=None):
        if job_id is not None:
                for job in jobs:
                        try:
                                if int(job.get("job_id")) == int(job_id):
                                        return job
                        except (TypeError, ValueError):
                                continue

        if name is not None:
                for job in jobs:
                        if str(job.get("name")) == str(name):
                                return job

        return None


def _needs_update(existing, desired_name, desired_method, desired_schedule_time, desired_schedule_days, force_update=False):
        if force_update or existing is None:
                return True

        if str(existing.get("name")) != str(desired_name):
                return True

        if str(existing.get("method")) != str(desired_method):
                return True

        existing_time = existing.get("schedule_time")
        if existing_time is not None and str(existing_time) != str(desired_schedule_time):
                return True

        if desired_schedule_days is not None:
                current_days = _normalize_days(existing.get("schedule_days"))
                if current_days != _normalize_days(desired_schedule_days):
                        return True

        return False


def run_module():
        module_args = dict(
                host=dict(type="str", required=True),
                client_key=dict(type="str", required=False),
                client_secret_key=dict(type="str", required=False, no_log=True),
                userid=dict(type="str", required=False),
                password=dict(type="str", required=False, no_log=True),
                proto=dict(type="str", required=False, default="https", choices=["http", "https"]),
                port=dict(type="int", required=False, default=4343),
                sslverify=dict(type="bool", required=False, default=True),
                debug=dict(type="bool", required=False, default=False),
                state=dict(type="str", required=False, default="present", choices=["present", "absent"]),
                name=dict(type="str", required=False),
                method=dict(type="str", required=False, choices=["1", "2", "3", "4"]),
                schedule_time=dict(type="str", required=False),
                job_id=dict(type="int", required=False),
                schedule_days=dict(type="str", required=False),
                force_update=dict(type="bool", required=False, default=False),
        )

        module = AnsibleModule(
                argument_spec=module_args,
                supports_check_mode=True,
                required_if=[
                        ("state", "present", ["name", "method", "schedule_time"]),
                        ("state", "absent", ["job_id"]),
                ],
        )

        result = dict(changed=False)

        helper = d42_backup_schedules(
                host=module.params["host"],
                module=module,
                result=result,
                sslverify=module.params["sslverify"],
                client_key=module.params["client_key"],
                client_secret_key=module.params["client_secret_key"],
                userid=module.params["userid"],
                password=module.params["password"],
                proto=module.params["proto"],
                port=module.params["port"],
                debug=module.params["debug"],
        )

        state = module.params["state"]

        jobs = _get_jobs(helper)
        existing = _find_job(
                jobs=jobs,
                job_id=module.params["job_id"],
                name=module.params["name"],
        )

        if state == "absent":
                if existing is None:
                        result["msg"] = "Backup schedule already absent"
                        module.exit_json(**result)

                resolved_job_id = int(existing.get("job_id"))
                result["changed"] = True
                result["api_backup_schedule"] = existing

                if module.check_mode:
                        result["msg"] = "Backup schedule would be deleted"
                        module.exit_json(**result)

                response = helper.d42_delete_backup_schedule(job_id=resolved_job_id)
                result["response"] = response
                module.exit_json(**result)

        needs_change = _needs_update(
                existing=existing,
                desired_name=module.params["name"],
                desired_method=module.params["method"],
                desired_schedule_time=module.params["schedule_time"],
                desired_schedule_days=module.params["schedule_days"],
                force_update=module.params["force_update"],
        )

        if not needs_change:
                result["api_backup_schedule"] = existing
                result["msg"] = "Backup schedule already in desired state"
                module.exit_json(**result)

        result["changed"] = True
        if module.check_mode:
                result["msg"] = "Backup schedule would be created/updated"
                if existing is not None:
                        result["api_backup_schedule"] = existing
                module.exit_json(**result)

        job_id_for_post = module.params["job_id"]
        if job_id_for_post is None and existing is not None:
                try:
                        job_id_for_post = int(existing.get("job_id"))
                except (TypeError, ValueError):
                        job_id_for_post = None

        response = helper.d42_post_backup_schedule(
                name=module.params["name"],
                method=module.params["method"],
                schedule_time=module.params["schedule_time"],
                job_id=job_id_for_post,
                schedule_days=module.params["schedule_days"],
        )
        result["response"] = response

        refreshed_jobs = _get_jobs(helper)
        resolved_job_id = _extract_job_id_from_response(response)
        result["api_backup_schedule"] = _find_job(
                jobs=refreshed_jobs,
                job_id=resolved_job_id or job_id_for_post,
                name=module.params["name"],
        )

        module.exit_json(**result)


def main():
        run_module()


if __name__ == "__main__":
        main()
