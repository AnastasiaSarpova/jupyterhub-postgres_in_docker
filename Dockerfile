FROM jupyterhub/jupyterhub:5.2.1

RUN pip install --no-cache \
oauthenticator \
dockerspawner \
jupyterhub-nativeauthenticators