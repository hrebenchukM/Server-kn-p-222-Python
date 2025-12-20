import base64, datetime, hashlib, hmac, json, random, string, uuid

from models.cgi_request import CgiRequest

def salt(len:int=16) -> str :
    symbols = string.ascii_letters + string.digits
    return "".join( random.choice(symbols) for _ in range(len) )


def hash(input:str) -> str :
    h = hashlib.sha256()
    h.update(input.encode('utf-8'))
    return h.hexdigest()


def kdf(password:str, salt:str) -> str :
    t = hash(password + salt)
    for _ in range(1000) :
        t = hash(t)
    return t[:32]    


def get_signature(data:bytes|str, key:bytes|None=None, alg:str="HS256", enc:str="base64url") -> str :
    if key is None :
        key = b"secret"  # TODO: перенести до змінних оточення або файлу-ініціалізатору

    if isinstance(data, str) :
        data = data.encode()

    if enc == "base64url" :
        match alg :
            case "HS256" :
                hash_alg = hashlib.sha256
            case "HS384" :
                hash_alg = hashlib.sha384
            case "HS512" :
                hash_alg = hashlib.sha512
            case _ :
                raise ValueError("Signature Algorythm not recognized: " + alg)    
        return base64.urlsafe_b64encode( 
            hmac.new(
                key,
                data,
                hash_alg
            ).digest()
        ).decode("ascii")
    else :
        raise ValueError("Encoder not recognized: " + enc)    

def b64u_decode(input:str) -> bytes :
    try :
        return base64.urlsafe_b64decode(input)
    except Exception :
        raise ValueError("JWT part is not valid Base64URL")

def b64u_to_json(input:str) -> any :
    return json.loads( base64.urlsafe_b64decode(input).decode() )


def json_to_b64u(input:any) -> str :
    return base64.urlsafe_b64encode(
        json.dumps(
            input, 
            ensure_ascii=False, 
            default=lambda o: o.__json__() if hasattr(o, '__json__') else str
        ).encode()
    ).decode("ascii")
   
def jwt_for_user(user:dict) -> str :
    '''
    Формує JWT на основі об'єкта користувача з БД
    '''
    if not isinstance(user, dict) :
        raise ValueError("User must be dict")

    return compose_jwt(
        sub = user.get('user_id'),
        claims = {
            'name':  user.get('user_name'),
            'email': user.get('user_email')
        }
    )

def validate_jwt(jwt:str) -> dict :
    '''
    JWT Validation by RFC 7519 sec.7.2
    '''
    if not isinstance(jwt, str) :
        raise ValueError("Parameter 'jwt' must be of type 'str'")

    # 1. перевірка на наявність "."
    if '.' not in jwt :
        raise ValueError("JWT must contain at least one period ('.')")

    parts = jwt.split('.')

    if len(parts) != 3 :
        raise ValueError("JWT must contain exactly 3 parts separated by '.'")

    # 2. header Base64
    try :
        header_bytes = b64u_decode(parts[0])
    except ValueError as err :
        raise ValueError("JWT header is not valid Base64URL")

    # 3. header UTF-8
    try :
        header_str = header_bytes.decode('utf-8')
    except Exception :
        raise ValueError("JWT header must be UTF-8 string")

    # 4. header JSON
    try :
        header = json.loads(header_str)
    except Exception :
        raise ValueError("JWT header must be valid JSON")

    if not isinstance(header, dict) :
        raise ValueError("JWT header must be an object")

    # 5. typ
    if header.get("typ") != "JWT" :
        raise ValueError("JWT header must contain 'typ' = 'JWT'")

    # 6. alg
    alg = header.get("alg")
    if alg is None :
        raise ValueError("JWT header must contain 'alg' field")

    # 7. перевірка підпису
    token_body = parts[0] + '.' + parts[1]
    if get_signature(token_body, alg=alg) != parts[2] :
        raise ValueError("JWT signature failure")

    # 8. payload
    payload = b64u_to_json(parts[1])
    if not isinstance(payload, dict) :
        raise ValueError("JWT payload must be valid JSON object")

    return payload


def authorize_request(req:CgiRequest) -> dict :
    '''
    Extract JWT from request, validate and return JWT payload

    Raise ValueError if authorization fails
    
    :return: JWT payload
    :rtype: dict
    '''
    auth_header = req.headers.get('Authorization', None)

    # 1. відсутній заголовок
    if auth_header is None :
        raise ValueError("Request must include 'Authorization' header")

    auth_scheme = 'Bearer '

    # 2. неправильна схема
    if not auth_header.startswith(auth_scheme) :
        raise ValueError("Authorization scheme must be Bearer")

    token = auth_header[len(auth_scheme):]

    return validate_jwt(token)



def authenticate_request(req:CgiRequest) -> tuple :
    auth_header = req.headers.get('Authorization', None)
    if not auth_header :
        raise ValueError("No 'Authorization' header in request")
    auth_scheme = 'Basic '
    if not auth_header.startswith(auth_scheme) :
        raise ValueError("Authorization scheme must be " + auth_scheme)
    credentials = base64.b64decode( auth_header[len(auth_scheme):] ).decode()
    if not ':' in credentials :
        raise ValueError("No separator ':' in credentials")
    return credentials.split(':', 1)


def compose_jwt(alg:str="HS256", typ:str="JWT", 
                iss:str|None="auto",
                sub:str|None=None,
                aud:str|None=None,
                exp:int|None=-1,
                nbf:int|None=None,
                iat:int|None=-1,
                jti:str|None="auto",
                claims:dict|None=None,
                signature_key:bytes|None=None
                ) -> str :
    token_header = {
        "alg": alg,
        "typ": typ
    }
    token_payload = {k:v for k, v in claims.items()
                     } if isinstance(claims, dict) else dict()
    if iss == 'auto' :
        token_payload['iss'] = "Server-KN-P-222"
    elif iss != None :
        token_payload['iss'] = iss

    if iat == -1 :
        token_payload['iat'] = int(datetime.datetime.now().timestamp())
    elif iat != None :
        token_payload['iat'] = iat

    if exp == -1 :
        if token_payload['iat'] != None :
            dt = datetime.datetime.fromtimestamp(token_payload['iat'])
            token_payload['exp'] = int( (dt + datetime.timedelta(minutes=1)).timestamp() )
    elif exp != None :
        token_payload['exp'] = exp

    if sub != None :
        token_payload['sub'] = sub
    if aud != None :
        token_payload['aud'] = aud
    if nbf != None :
        token_payload['nbf'] = nbf

    if jti == 'auto' :
        token_payload['jti'] = str(uuid.uuid4())
    elif jti != None :
        token_payload['jti'] = jti
    #return json_to_b64u(token_payload) + '.' + json_to_b64u(token_payload)

    if not typ in ("JWT", "JWS") :
        raise NotImplementedError()
    
    token_body = ( 
        json_to_b64u(token_header)
        + '.' 
        + json_to_b64u(token_payload)
    )
    return token_body + '.' + get_signature(token_body, alg=alg, key=signature_key)
        



def main() :
    try :
        print(validate_jwt('eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJqdGkiOiAiYzhkMGFkYjUtYWFhOS00OGJkLWIzYzEtNjE2Y2M2MWVkNTU2IiwgInN1YiI6ICI2OTIzMWM1NS05ODUxLTExZjAtYjFiNy02MjUxNzYwMDU5NmMiLCAiaWF0IjogMTc2NTI3OTM1NCwgImV4cCI6IDE3NjUyNzk0MTQsICJuYW1lIjogIkRlZmF1bHQgQWRtaW5pc3RyYXRvciIsICJlbWFpbCI6ICJhZG1pbkBsb2NhbGhvc3QifQ==.fIeR5m8SK_2urLp6ZRMYz_pXqmuKT1BZTq7EfjLj9sY='))
    except ValueError as err :
        print(err)


if __name__ == "__main__" :
    main()

