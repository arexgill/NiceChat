from google.cloud import aiplatform
import vertexai
from vertexai.preview.language_models import TextGenerationModel


temperature = 0.1
vertexai.init(project="tactical-runway-407513", location='us-central1')

parameters = {
    "temperature": temperature,  # Temperature controls the degree of randomness in token selection.
    "max_output_tokens": 256,  # Token limit determines the maximum amount of text output.
    "top_p": 0.8,
    # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
    "top_k": 40,  # A top_k of 1 means the selected token is the most probable among all tokens.
}
model = TextGenerationModel.from_pretrained("text-bison@001")


class Convo:
    def __init__(self):
        self._model = model
        context = parameters.pop('context', None)
        self._parameters = parameters
        self._requests = []
        self._replies = []
        if context:
            self._context = context
        else:
            self._context = []

    def predict(self, prompt: str, grounding=''):
        try:
            gs = vertexai.language_models._language_models.VertexAISearch(grounding, 'global')
            response = self._model.predict(
                '\n'.join(self._context + [prompt]), grounding_source = gs,
                **self._parameters,
            )
        except Exception as e:
            err = f"Bot couldn't retrieve an answer: {e}"
            print(err)
            return err
        return response.text

    def converse(self, prompt: str):
        self._requests.append(prompt)
        prompt_parts = self._requests[:1] + self._replies + [prompt]
        response = self.predict('\n'.join(prompt_parts))
        self._replies.append(response.text)
        return response

    def add_context(self, *context_strs):
        self._context.extend(context_strs)