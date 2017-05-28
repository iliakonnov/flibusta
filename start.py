#!/usr/bin/python3
from webserver import app
app.config['zippath'] = '/media/d-link/Transmission/complete/fb2.Flibusta.Net'
app.run(host='0.0.0.0', port=13208, debug=False)
