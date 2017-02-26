# Servidor del proyecto Fixit

Actualmente este servidor es un api rest que consume la aplicación móvil. La seguridad se maneja por tokens. Esto significa que hay que hacer una petición inicial a  api-token-auth/ para obenet el token. Una vez se tiene el token todas las peticiones posteriores deben ser enviadas utilizando el encabezdo Authorization: token <token obtenido> a cada uno de los endpoints
