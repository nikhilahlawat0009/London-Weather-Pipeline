# Start Flask app in a separate thread
thread = threading.Thread(target=run_app)
thread.daemon = True
thread.start()

# Display a clickable link to the Flask app
display(HTML("<a href='http://127.0.0.1:5000' target='_blank'>Click here to open the app</a>"))
