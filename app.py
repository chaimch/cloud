from exts.cloudflask import CloudFlask

app = CloudFlask.create_app(config_dot_path='config.DevConfig')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
