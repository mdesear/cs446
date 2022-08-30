#Set up a docker environment for this code, and don't try to include superfluous packages!
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import random
import os
import socket
from OpenSSL import crypto, SSL

blackblankimage = random.randint(0, 255) * np.ones(shape=[512, 512, 3], dtype=np.uint8)

cv.putText(blackblankimage, "You did it!", (100, 100), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255))
cv.rectangle(blackblankimage, pt1=(200,200), pt2=(300, 300), color=(0,0,255), thickness=-1)
plt.axis('off')
plt.imshow(blackblankimage)

plt.savefig("./pythonCode1Image.png")

#modify this code so that it also generates self signed certificate and keys

def certGen (
	countryName = "US",
	stateName = "NV",
	cityName = "Reno",
	organizationName = "University of Nevada, Reno",
	organizationUnitName = "CSE",
	commonName = socket.gethostname(),
	serialNum = 42,
	validityEndInSecs = 5*365*24*60*60,
	KEY_FILE = "gdesear_privateKey.PEM",
	CERT_FILE = "gdesear_selfSignedCertificate.PEM"
	):
	
	k = crypto.PKey()
	k.generate_key(crypto.TYPE_RSA, 2048)
	
	cert = crypto.X509()
	cert.get_subject().C = countryName
	cert.get_subject().ST = stateName
	cert.get_subject().O = organizationName
	cert.get_subject().OU = organizationUnitName
	cert.get_subject().CN = commonName
	cert.set_serial_number(serialNum)
	cert.gmtime_adj_notBefore(0)
	cert.gmtime_adj_notAfter(validityEndInSecs)
	cert.set_issuer(cert.get_subject())
	cert.set_pubkey(k)
	cert.sign(k, 'sha512')
	with open (CERT_FILE, "wt") as f:
		f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))
	with open (KEY_FILE, "wt") as f:
		f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode("utf-8"))
	
	os.system("openssl rsa -in gdesear_privateKey.PEM -pubout -out gdesear_publicKey.key")
	
	print(str((cert.get_signature_algorithm())))
	
certGen()

