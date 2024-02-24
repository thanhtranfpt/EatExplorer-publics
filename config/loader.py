import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import google.generativeai as genai



class Configs:
    def __init__(self, firebase_service_account_keys_file,
                 gemini_api_key) -> None:
        self.firebase_service_account_keys_file = firebase_service_account_keys_file
        self.gemini_api_key = gemini_api_key

        self.initialize_firebase_firestore()
        self.initialize_gemini()


    def initialize_firebase_firestore(self):
        # Cloud Firestore
        cred = credentials.Certificate(self.firebase_service_account_keys_file)
        app = firebase_admin.initialize_app(cred)
        db = firestore.client()
        users_ref = db.collection('users')

        self.users_ref = users_ref

    def initialize_firebase_storage(self):
        # Google Firebase configs
        firebaseConfig = {
        }

        firebase = pyrebase.initialize_app(config=firebaseConfig)
        storage = firebase.storage()

        self.storage = storage


    def initialize_gemini(self):
        genai.configure(api_key=self.gemini_api_key)

        # Set up the model
        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
            }
        
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]

        model = genai.GenerativeModel(model_name="gemini-pro",
                                      generation_config=generation_config,
                                      safety_settings=safety_settings)
        

        self.gemini_model = model




configs = Configs(firebase_service_account_keys_file='config/secrets/eatexplorer-4396c-firebase-adminsdk-txbnp-4f93353d0d.json',
                  gemini_api_key="***************************************")