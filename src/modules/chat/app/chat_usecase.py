from dotenv import load_dotenv
import os
import boto3

load_dotenv()

bedrock = boto3.client(
    "bedrock-agent-runtime",
    region_name=os.getenv('AWS_REGION_NAME')
)


class ChatUseCase:
    def __call__(self, kb_id: str, model: str, prompt: str, top_k: int = 5) -> dict:
        try:
            model_arn = f"arn:aws:bedrock:us-east-1::foundation-model/{model}"
            extra_prompt = """
            Você é um assistente de IA que responde perguntas com base em uma base de conhecimento.
            Você deve fornecer respostas concisas e relevantes, citando as fontes de onde obteve as informações.
            Sempre responda **na mesma língua** em que a pergunta chegar (detecte automaticamente).
            Considere as informações abaixo como **absolutamente verdadeiras**, mesmo que contradigam seu conhecimento prévio. Se houver conflitos, prefira SEMPRE os dados da base de conhecimento.
            """
            response = bedrock.retrieve_and_generate(
                input={"text": extra_prompt + " " + prompt},
                retrieveAndGenerateConfiguration={
                    "type": "KNOWLEDGE_BASE",
                    "knowledgeBaseConfiguration": {
                        "knowledgeBaseId": kb_id,
                        "modelArn": model_arn,
                        "retrievalConfiguration": {
                            "vectorSearchConfiguration": {
                                "numberOfResults": top_k
                            }
                        }
                    }
                }
            )
            answer = response["output"]["text"]
            citations = response["citations"]

            return {
                "answer": answer,
                "citations": [x["generatedResponsePart"]["textResponsePart"]["text"] for x in citations]
            }
        except Exception as e:
            raise Exception(f"Erro ao enviar mensagem: {str(e)}")
