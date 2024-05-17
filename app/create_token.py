from middlewares.check_api_token import generate_token
import yaml

token = generate_token()
print(yaml.dump(token, default_flow_style=False))
