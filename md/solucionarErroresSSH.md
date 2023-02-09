# Warning: Remote Host Identification Has Changed
* Abrir en vim el archivo $HOME/.ssh/known_hosts
* Eliminar las llaves en ese archivo

# diffie-hellman-group1-sha1
* Abrir en vim el archivo $HOME/.ssh/config
* Añadir el siguiente codigo

    HOST "direccion_ip_a_conectar"
        KexAlgorithms diffie-hellman-group1-sha1,curve25519-sha256@libssh.org,ecdh-sha2-nistp256,ecdh-sha2-nistp384,ecdh-sha2-nistp521,diffie-hellman-group-exchange-sha256,diffie-hellman-group14-sha1
        Ciphers 3des-cbc,blowfish-cbc,aes128-cbc,aes128-ctr,aes256-ctr