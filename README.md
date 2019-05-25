# PlayShikiServer
A server side app restoring old play.shikimori.org functionality

# PlayShikiServer - a server-side application restoring old play.shikimori.org functionality
### Installation

PlayShikiServer requires [Python 3](https://www.python.org/downloads/release/python-373/)  to run.

Install the dependencies:

```sh
cd PlayShikiServer
pip3 install -r requerements.txt
cd ..
git clone https://github.com/PlayShikimoriApp/PlayShikiClient
```

Restore database from backup:

```
cat db/dump_example.sql | sqlite3 db-test.sqlite
```

Generate keys (used for server responses encoding):
```
./utils/genkeys.py 2048 key.priv
./utils/genkeys.py $(( 64 * 1024 )) key2.priv
```

Encode database URLs:
```
./encode_db_urls.py key.priv
cp key.priv ../PlayShikiClient
cp key2.priv ../PlayShikiClient
```

# Configure client-side application:

Install dependencies
```
cd ../PlayShikiClient
npm install
sudo npm install -g pkg
```

Generate *.js keys:
```
./utils/genkeys.py key.priv keys/key.js
./utils/genkeys.py key2.priv keys/key2.js
```

Configure host address and port in .env file
```
HOST=127.0.0.1
PORT=8100
```

# Start server

Now start the server:
```
cd ../PlayShikiServer
nohup runserver.py &
```

# Client app packaging and run
```
cd ../PlayShikiClient
pkg .
```

Run Shikimori.exe and leave it running in background.
