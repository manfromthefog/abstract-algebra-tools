from django.shortcuts import render
from django.http import JsonResponse
from . import rsa
import json

MAX_INPUT = 10000

# Create your views here.
def index(request):
    return render(request, 'rsa/index.html', {'max_input': MAX_INPUT})

def generate_keys(request):
    """Post endpoint to generate RSA keys"""
    if (request.method != "POST"):
        return JsonResponse({"error" : "Invalid request"}, status=400)
    try:
        data = json.loads(request.body)
        p = int(data.get("p"))
        q = int(data.get("q"))
    except Exception:
        return JsonResponse({"error": "Invalid input"}, status=400)

    if any(abs(x) > MAX_INPUT for x in (p, q)):
        return JsonResponse({"error": f"Inputs must be <= {MAX_INPUT}"}, status=400)

    if not rsa.is_prime(p) or not rsa.is_prime(q):
        return JsonResponse({"error": "p and q must both be prime"}, status=400)
    
    keys = rsa.gen_keys(p, q)

    # return as ints
    return JsonResponse({
        "n" : keys["n"],
        "m" : keys["m"],
        "e" : keys["e"],
        "d" : keys["d"],
    })

def encrypt(request):
    """Post endpoint {M, e, n} -> return ciphertext C"""
    if (request.method != "POST"):
        return JsonResponse({"error" : "Invalid request"}, status=400)
    
    try:
        data = json.loads(request.body)
        M = int(data.get("M"))
        e = int(data.get("e"))
        n = int(data.get("n"))
    except Exception:
        return JsonResponse({"error" : "Invalid input"}, status=400)

    if abs(M) > MAX_INPUT:
        return JsonResponse({"error": f"Message must be <= {MAX_INPUT}"}, status=400)
    
    C = rsa.encrypt_integer(M,e,n)
    return JsonResponse({"C":C})

def decrypt(request):
    """Post endpoint {C, d, n} -> returns {R}"""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)
    try:
        data = json.loads(request.body)
        C = int(data.get("C"))
        d = int(data.get("d"))
        n = int(data.get("n"))
    except Exception:
        return JsonResponse({"error": "Invalid input"}, status=400)

    R = rsa.decrypt_integer(C % n, d, n)
    return JsonResponse({"R": R})