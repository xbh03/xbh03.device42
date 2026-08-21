#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_certificates
short_description: Manage Device42 certificates
description:
    - Create, update, or delete Device42 certificates.
    - Supports C(POST /api/1.0/certificates/), C(DELETE /api/1.0/certificates/{ID}/),
        and C(PUT /api/1.0/custom_fields/certificate/).
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
            - Device42 API port.
        required: false
        type: int
        default: 443
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
            - Desired state of the certificate.
        required: false
        type: str
        default: present
        choices:
            - present
            - absent
    present_endpoint:
        description:
            - Endpoint used when C(state=present).
            - C(post) uses C(/api/1.0/certificates/).
            - C(custom_fields) uses C(/api/1.0/custom_fields/certificate/).
        required: false
        type: str
        default: post
        choices:
            - post
            - custom_fields
    force_update:
        description:
            - Force update call when C(state=present) even if no drift is detected.
        required: false
        type: bool
        default: false
    certificate_id:
        description:
            - Certificate numeric ID.
            - Required when C(state=absent).
        required: false
        type: str
    dns:
        description:
            - DNS address of the site the certificate is issued for.
            - When provided, this is the only required field for creating a new certificate.
        required: false
        type: str
    issued_to:
        description:
            - Entity certificate is issued to.
        required: false
        type: str
    issued_by:
        description:
            - Entity issuing the certificate.
        required: false
        type: str
    valid_from:
        description:
            - Start date of the certificate in YYYY-MM-DD format.
            - Required when creating a new certificate without C(dns).
        required: false
        type: str
    valid_to:
        description:
            - Expiration date of the certificate in YYYY-MM-DD format.
            - Required when creating a new certificate without C(dns).
        required: false
        type: str
    subject:
        description:
            - Person or entity identified.
        required: false
        type: str
    version:
        description:
            - Version of the encoded certificate.
        required: false
        type: str
    serial_number:
        description:
            - Unique identifier of the certificate.
        required: false
        type: str
    signature_algorithm:
        description:
            - Algorithm used to create the signature.
        required: false
        type: str
    signature_hash:
        description:
            - Actual signature to verify that it came from the issuer.
        required: false
        type: str
    san:
        description:
            - Subject Alternative Name.
        required: false
        type: str
    digital_signature_usage:
        description:
            - Subject public key is used for verifying digital signatures.
        required: false
        type: str
        choices:
            - yes
            - no
    content_commitment_usage:
        description:
            - Content commitment usage flag.
        required: false
        type: str
        choices:
            - yes
            - no
    key_encipherment_usage:
        description:
            - Subject public key is used for enciphering private or secret keys.
        required: false
        type: str
        choices:
            - yes
            - no
    data_encipherment_usage:
        description:
            - Subject public key is used for directly enciphering raw user data.
        required: false
        type: str
        choices:
            - yes
            - no
    key_agreement_usage:
        description:
            - Subject public key is used for key agreement.
        required: false
        type: str
        choices:
            - yes
            - no
    key_cert_sign_usage:
        description:
            - Subject public key is used for verifying signatures on public key certificates.
        required: false
        type: str
        choices:
            - yes
            - no
    crl_sign_usage:
        description:
            - Subject public key is used for verifying signatures on certificate revocation lists.
        required: false
        type: str
        choices:
            - yes
            - no
    encipher_only_usage:
        description:
            - Subject public key may be used only for enciphering data while performing key agreement.
        required: false
        type: str
        choices:
            - yes
            - no
    decipher_only_usage:
        description:
            - Subject public key may be used only for deciphering data while performing key agreement.
        required: false
        type: str
        choices:
            - yes
            - no
    extended_key_usage:
        description:
            - Purpose of the public key contained in the certificate.
        required: false
        type: str
        choices:
            - yes
            - no
    vendor:
        description:
            - Name of the vendor that provided this certificate.
        required: false
        type: str
    end_point_type:
        description:
            - Certificate endpoint type.
        required: false
        type: str
    end_point_id:
        description:
            - Certificate endpoint ID.
        required: false
        type: str
    groups:
        description:
            - Multitenancy admin groups access string.
        required: false
        type: str
    tags:
        description:
            - Comma-separated list of tags to add.
        required: false
        type: str
    tags_remove:
        description:
            - Comma-separated list of tags to remove.
        required: false
        type: str
    custom_field_key:
        description:
            - Custom field key for C(present_endpoint=custom_fields).
        required: false
        type: str
    custom_field_name:
        description:
            - Certificate name for custom field update (alternative to C(certificate_id)).
        required: false
        type: str
    custom_field_type:
        description:
            - Custom field type.
        required: false
        type: str
    custom_field_mandatory:
        description:
            - Whether custom field is mandatory, C(yes) or C(no).
        required: false
        type: str
        choices:
            - yes
            - no
    custom_field_filterable:
        description:
            - Whether custom field is filterable, C(yes) or C(no).
        required: false
        type: str
        choices:
            - yes
            - no
    custom_field_log_for_api:
        description:
            - Whether custom field is logged for API, C(yes) or C(no).
        required: false
        type: str
        choices:
            - yes
            - no
    custom_field_related_field_name:
        description:
            - Related field name for related_field custom type.
        required: false
        type: str
    custom_field_add_to_picklist:
        description:
            - Comma-separated values to add to picklist.
        required: false
        type: str
    custom_field_remove_from_picklist:
        description:
            - Comma-separated values to remove from picklist.
        required: false
        type: str
    custom_field_delete_in_use:
        description:
            - Delete in-use picklist values, C(yes) or C(no).
        required: false
        type: str
        choices:
            - yes
            - no
    custom_field_related_field_value_by_id:
        description:
            - Set related field by ID, C(yes) or C(no).
        required: false
        type: str
        choices:
            - yes
            - no
    custom_field_value:
        description:
            - Custom field value.
        required: false
        type: str
    custom_field_clear_value:
        description:
            - Clear custom field value, C(yes) or C(no).
        required: false
        type: str
        choices:
            - yes
            - no
    custom_field_notes:
        description:
            - Custom field notes.
        required: false
        type: str
    custom_field_clear_notes:
        description:
            - Clear custom field notes, C(yes) or C(no).
        required: false
        type: str
        choices:
            - yes
            - no
    custom_field_bulk_fields:
        description:
            - Bulk custom key:value pairs.
        required: false
        type: str
    custom_field_multi_select:
        description:
            - Picklist multi-select, C(yes) or C(no).
        required: false
        type: str
        choices:
            - yes
            - no
"""

EXAMPLES = r"""
- name: Create certificate by DNS
    xbh03.device42.certificates.d42_api_certificates:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: present
        present_endpoint: post
        dns: test.device42.com

- name: Create certificate by validity dates
    xbh03.device42.certificates.d42_api_certificates:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: present
        present_endpoint: post
        issued_to: registration.device42.com
        valid_from: "2024-01-01"
        valid_to: "2027-01-01"
        serial_number: 77eb9b55e9228635f2157fd374b8da8

- name: Update certificate custom field
    xbh03.device42.certificates.d42_api_certificates:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: present
        present_endpoint: custom_fields
        certificate_id: "3"
        custom_field_key: Environment
        custom_field_type: text
        custom_field_value: Production

- name: Delete certificate
    xbh03.device42.certificates.d42_api_certificates:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: absent
        certificate_id: "114"
"""

RETURN = r"""
api_certificate:
    description: Current or resulting certificate data when available.
    type: dict
    returned: success
response:
    description: Raw response from Device42 for create/update/delete/custom field operations.
    type: dict
    returned: when changed
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.certificates.d42_certificates import (
        d42_certificates,
)


def _extract_certificate_id_from_response(response):
        if not isinstance(response, dict):
                return None

        msg = response.get("msg")
        if isinstance(msg, list) and len(msg) > 1:
                try:
                        return str(msg[1])
                except (TypeError, ValueError):
                        return None

        for key in ("id", "certificate_id"):
                if response.get(key) is not None:
                        return str(response.get(key))

        return None


def _find_certificate(helper, certificate_id=None, serial_number=None, dns=None):
        payload = helper.d42_get_certificates(certificate_id=certificate_id)
        candidates = payload.get("certificate_details", [])

        if certificate_id is not None:
                for cert in candidates:
                        if str(cert.get("id")) == str(certificate_id):
                                return cert

        if serial_number is not None:
                all_certs = helper.d42_get_certificates().get("certificate_details", [])
                for cert in all_certs:
                        if str(cert.get("serial_number")) == str(serial_number):
                                return cert

        if dns is not None:
                all_certs = helper.d42_get_certificates().get("certificate_details", [])
                for cert in all_certs:
                        if str(cert.get("issued_to")) == str(dns):
                                return cert

        return None


def _build_post_payload(params):
        keys = [
                "id",
                "dns",
                "issued_to",
                "issued_by",
                "valid_from",
                "valid_to",
                "subject",
                "version",
                "serial_number",
                "signature_algorithm",
                "signature_hash",
                "san",
                "digital_signature_usage",
                "content_commitment_usage",
                "key_encipherment_usage",
                "data_encipherment_usage",
                "key_agreement_usage",
                "key_cert_sign_usage",
                "crl_sign_usage",
                "encipher_only_usage",
                "decipher_only_usage",
                "extended_key_usage",
                "vendor",
                "end_point_type",
                "end_point_id",
                "groups",
                "tags",
                "tags_remove",
        ]

        payload = {}
        for key in keys:
                value = params.get(key)
                if value is not None:
                        payload[key] = value
        return payload


def _needs_update(existing, payload, force_update=False):
        if force_update or existing is None:
                return True

        always_change_keys = {"groups", "tags_remove"}

        for key, desired in payload.items():
                if key in always_change_keys:
                        return True
                if key == "id":
                        continue
                current = existing.get(key)
                if str(current) != str(desired):
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
                port=dict(type="int", required=False, default=443),
                sslverify=dict(type="bool", required=False, default=True),
                debug=dict(type="bool", required=False, default=False),
                state=dict(type="str", required=False, default="present", choices=["present", "absent"]),
                present_endpoint=dict(type="str", required=False, default="post", choices=["post", "custom_fields"]),
                force_update=dict(type="bool", required=False, default=False),
                certificate_id=dict(type="str", required=False),
                dns=dict(type="str", required=False),
                issued_to=dict(type="str", required=False),
                issued_by=dict(type="str", required=False),
                valid_from=dict(type="str", required=False),
                valid_to=dict(type="str", required=False),
                subject=dict(type="str", required=False),
                version=dict(type="str", required=False),
                serial_number=dict(type="str", required=False),
                signature_algorithm=dict(type="str", required=False),
                signature_hash=dict(type="str", required=False),
                san=dict(type="str", required=False),
                digital_signature_usage=dict(type="str", required=False, choices=["yes", "no"]),
                content_commitment_usage=dict(type="str", required=False, choices=["yes", "no"]),
                key_encipherment_usage=dict(type="str", required=False, choices=["yes", "no"]),
                data_encipherment_usage=dict(type="str", required=False, choices=["yes", "no"]),
                key_agreement_usage=dict(type="str", required=False, choices=["yes", "no"]),
                key_cert_sign_usage=dict(type="str", required=False, choices=["yes", "no"]),
                crl_sign_usage=dict(type="str", required=False, choices=["yes", "no"]),
                encipher_only_usage=dict(type="str", required=False, choices=["yes", "no"]),
                decipher_only_usage=dict(type="str", required=False, choices=["yes", "no"]),
                extended_key_usage=dict(type="str", required=False, choices=["yes", "no"]),
                vendor=dict(type="str", required=False),
                end_point_type=dict(type="str", required=False),
                end_point_id=dict(type="str", required=False),
                groups=dict(type="str", required=False),
                tags=dict(type="str", required=False),
                tags_remove=dict(type="str", required=False),
                custom_field_key=dict(type="str", required=False),
                custom_field_name=dict(type="str", required=False),
                custom_field_type=dict(type="str", required=False),
                custom_field_mandatory=dict(type="str", required=False, choices=["yes", "no"]),
                custom_field_filterable=dict(type="str", required=False, choices=["yes", "no"]),
                custom_field_log_for_api=dict(type="str", required=False, choices=["yes", "no"]),
                custom_field_related_field_name=dict(type="str", required=False),
                custom_field_add_to_picklist=dict(type="str", required=False),
                custom_field_remove_from_picklist=dict(type="str", required=False),
                custom_field_delete_in_use=dict(type="str", required=False, choices=["yes", "no"]),
                custom_field_related_field_value_by_id=dict(type="str", required=False, choices=["yes", "no"]),
                custom_field_value=dict(type="str", required=False),
                custom_field_clear_value=dict(type="str", required=False, choices=["yes", "no"]),
                custom_field_notes=dict(type="str", required=False),
                custom_field_clear_notes=dict(type="str", required=False, choices=["yes", "no"]),
                custom_field_bulk_fields=dict(type="str", required=False),
                custom_field_multi_select=dict(type="str", required=False, choices=["yes", "no"]),
        )

        module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
        result = dict(changed=False)

        helper = d42_certificates(
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
        present_endpoint = module.params["present_endpoint"]

        existing = _find_certificate(
                helper=helper,
                certificate_id=module.params["certificate_id"],
                serial_number=module.params["serial_number"],
                dns=module.params["dns"],
        )

        if state == "absent":
                if module.params["certificate_id"] is None:
                        module.fail_json(msg="certificate_id is required when state=absent.")

                if existing is None:
                        result["msg"] = "Certificate already absent"
                        module.exit_json(**result)

                result["changed"] = True
                result["api_certificate"] = existing

                if module.check_mode:
                        result["msg"] = "Certificate would be deleted"
                        module.exit_json(**result)

                response = helper.d42_delete_certificate(certificate_id=module.params["certificate_id"])
                result["response"] = response
                module.exit_json(**result)

        if present_endpoint == "custom_fields":
                if not module.params["custom_field_key"]:
                        module.fail_json(msg="custom_field_key is required when present_endpoint=custom_fields.")

                cert_id = module.params["certificate_id"]
                cert_name = module.params["custom_field_name"]
                if cert_id is None and cert_name is None:
                        module.fail_json(msg="certificate_id or custom_field_name is required when present_endpoint=custom_fields.")

                result["changed"] = True
                if module.check_mode:
                        result["msg"] = "Certificate custom fields would be updated"
                        if existing is not None:
                                result["api_certificate"] = existing
                        module.exit_json(**result)

                response = helper.d42_put_custom_field_certificate(
                        key=module.params["custom_field_key"],
                        certificate_id=int(cert_id) if cert_id is not None else None,
                        name=cert_name,
                        type=module.params["custom_field_type"],
                        mandatory=module.params["custom_field_mandatory"],
                        filterable=module.params["custom_field_filterable"],
                        log_for_api=module.params["custom_field_log_for_api"],
                        related_field_name=module.params["custom_field_related_field_name"],
                        add_to_picklist=module.params["custom_field_add_to_picklist"],
                        remove_from_picklist=module.params["custom_field_remove_from_picklist"],
                        delete_in_use=module.params["custom_field_delete_in_use"],
                        related_field_value_by_id=module.params["custom_field_related_field_value_by_id"],
                        value=module.params["custom_field_value"],
                        clear_value=module.params["custom_field_clear_value"],
                        notes=module.params["custom_field_notes"],
                        clear_notes=module.params["custom_field_clear_notes"],
                        bulk_fields=module.params["custom_field_bulk_fields"],
                        multi_select=module.params["custom_field_multi_select"],
                )
                result["response"] = response

                resolved_id = cert_id or _extract_certificate_id_from_response(response)
                if resolved_id is not None:
                        result["api_certificate"] = _find_certificate(helper=helper, certificate_id=resolved_id)
                else:
                        result["api_certificate"] = existing
                module.exit_json(**result)

        post_payload = _build_post_payload(
                {
                        "id": module.params["certificate_id"],
                        "dns": module.params["dns"],
                        "issued_to": module.params["issued_to"],
                        "issued_by": module.params["issued_by"],
                        "valid_from": module.params["valid_from"],
                        "valid_to": module.params["valid_to"],
                        "subject": module.params["subject"],
                        "version": module.params["version"],
                        "serial_number": module.params["serial_number"],
                        "signature_algorithm": module.params["signature_algorithm"],
                        "signature_hash": module.params["signature_hash"],
                        "san": module.params["san"],
                        "digital_signature_usage": module.params["digital_signature_usage"],
                        "content_commitment_usage": module.params["content_commitment_usage"],
                        "key_encipherment_usage": module.params["key_encipherment_usage"],
                        "data_encipherment_usage": module.params["data_encipherment_usage"],
                        "key_agreement_usage": module.params["key_agreement_usage"],
                        "key_cert_sign_usage": module.params["key_cert_sign_usage"],
                        "crl_sign_usage": module.params["crl_sign_usage"],
                        "encipher_only_usage": module.params["encipher_only_usage"],
                        "decipher_only_usage": module.params["decipher_only_usage"],
                        "extended_key_usage": module.params["extended_key_usage"],
                        "vendor": module.params["vendor"],
                        "end_point_type": module.params["end_point_type"],
                        "end_point_id": module.params["end_point_id"],
                        "groups": module.params["groups"],
                        "tags": module.params["tags"],
                        "tags_remove": module.params["tags_remove"],
                }
        )

        if not post_payload:
                module.fail_json(msg="At least one parameter is required when present_endpoint=post.")

        if existing is None and module.params["dns"] is None:
                if module.params["valid_from"] is None or module.params["valid_to"] is None:
                        module.fail_json(msg="valid_from and valid_to are required when creating a new certificate without dns.")

        needs_change = _needs_update(
                existing=existing,
                payload=post_payload,
                force_update=module.params["force_update"],
        )

        if not needs_change:
                result["api_certificate"] = existing
                result["msg"] = "Certificate already in desired state"
                module.exit_json(**result)

        result["changed"] = True
        if module.check_mode:
                result["msg"] = "Certificate would be created/updated"
                if existing is not None:
                        result["api_certificate"] = existing
                module.exit_json(**result)

        response = helper.d42_post_certificates(**post_payload)
        result["response"] = response

        resolved_id = _extract_certificate_id_from_response(response) or module.params["certificate_id"]
        result["api_certificate"] = _find_certificate(
                helper=helper,
                certificate_id=resolved_id,
                serial_number=module.params["serial_number"],
                dns=module.params["dns"],
        )

        module.exit_json(**result)


def main():
        run_module()


if __name__ == "__main__":
        main()
