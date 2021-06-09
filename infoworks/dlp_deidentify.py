import google.cloud.dlp
from google.oauth2 import service_account
import base64
key_path = "/Users/infoworks/Downloads/gcp-cs-shared-resources-be01d4b5a458.json"
credentials = service_account.Credentials.from_service_account_file(key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],)


dlp_client = google.cloud.dlp_v2.DlpServiceClient(credentials=credentials)
project_id = 'gcp-cs-shared-resources'
#location = 'PROJECT_LOCATION'


# Function to use
def deterministicDeidentifyWithFpe(dlp_client, parent, text, info_types, surrogate_type, wrapped_key=None):
    """Uses the Data Loss Prevention API to deidentify sensitive data in a
    string using Format Preserving Encryption (FPE).
    Args:
        dlp_client: DLP Client instantiation
        parent: str - The parent resource name, for example projects/my-project-id.
        text: str - text to deidentify
        info_types: list type of sensitive data, such as a name, email address, telephone number, identification number,
        or credit card number.  https://cloud.google.com/dlp/docs/infotypes-reference
        surrogate_type: The name of the surrogate custom info type to use. Only
            necessary if you want to reverse the deidentification process. Can
            be essentially any arbitrary string, as long as it doesn't appear
            in your dataset otherwise.
        wrapped_key: The encrypted ('wrapped') AES-256 key to use (bytes that was encoded in base64).
        This key should be encrypted using a Cloud KMS key.
    Returns:
        None; the response from the API is printed to the terminal.
    """
    # The wrapped key is base64-encoded, but the library expects a binary
    # string, so decode it here.
    wrapped_key = base64.b64decode(wrapped_key)

    # Construct inspect configuration dictionary
    inspect_config = {
        "info_types": [{"name": info_type} for info_type in info_types]
    }

    # Construct deidentify configuration dictionary
    deidentify_config = {
        "info_type_transformations": {
            "transformations": [
                {
                    "primitive_transformation": {
                        "crypto_deterministic_config": {
                            "crypto_key": {
                                "unwrapped": {
                                    "key": wrapped_key
                                }
                            },
                            'surrogate_info_type': {"name": surrogate_type}
                        },

                    }
                }
            ]
        }
    }

    # Convert string to item
    item = {"value": text}

    # Call the API
    response = dlp_client.deidentify_content(
        request={
            "parent": parent,
            "deidentify_config": deidentify_config,
            "inspect_config": inspect_config,
            "item": item,
        }
    )

    # Print results
    print('Successful Redaction.')
    return response.item.value


# Dummy input
parent = f"projects/{project_id}"
#doctors_notes = 'COVID-19: case 24\nIzzo Andrea, DʼAversa Lucia, Ceremonial Giuseppe, Mazzella Giuseppe, Pergoli Pericle, Faiola Eugenio Leone, Di Pastena Francesca\nU.O.C. Diagnostic imaging - “Dono Svizzero” Hospital Formia DEA I level‒ Latin Asl\nPc woman, 78 years old, transported since 118 from another hospital, I was insu fficent for acute acute spi ry. Conscious, tachypnoic, apyretic P z with 50% pO2. Chest x-ray required, hospitalized in resuscitation and predisposed to nasopharyngeal swab (COVID-19 positive).\nchest X-ray\nD SUP\n'
#doctors_notes = 'COVID-19: case 24 \nIzzo Andrea, DʼAversa Lucia, abhishek@gmail.com 4354190902342056'
doctors_notes = 'COVID-19: email: abhishek@gmail.com phone: 8015760129'

INFO_TYPES = ["FIRST_NAME", "LAST_NAME", "FEMALE_NAME", "MALE_NAME", "PERSON_NAME", "STREET_ADDRESS",
              "ITALY_FISCAL_CODE", "EMAIL_ADDRESS", "PHONE_NUMBER"]
AES256_key = "x8v/a?f(K+KLdeSh"
AES256_key_bytes = base64.b64encode(AES256_key.encode('utf-8'))

# Run de-identification
encrypted_raw_txt_string = deterministicDeidentifyWithFpe(dlp_client=dlp_client,
                                                          parent=parent,
                                                          text=doctors_notes,
                                                          info_types=INFO_TYPES,
                                                          surrogate_type="REDACTED",
                                                          wrapped_key=AES256_key_bytes)

print(encrypted_raw_txt_string)