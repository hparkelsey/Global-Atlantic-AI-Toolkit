# Start-Process -NoNewWindow -FilePath "python" -ArgumentList "C:\Users\hoyun\Downloads\CLSentimentAnalysis\CLSA-vF\app\script.py"
# Start-Process -NoNewWindow -WorkingDirectory "C:\Users\hoyun\Downloads\CLSentimentAnalysis\CLSA-vF\app" -FilePath "npm" -ArgumentList "start"

# Start-Process "http://localhost:19000"

# Get the script's directory
$scriptDir = $PSScriptRoot

# Start Python script
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "$scriptDir\script.py"

# Start React Native app
Start-Process -NoNewWindow -WorkingDirectory $scriptDir -FilePath "npm" -ArgumentList "start"

# Open web view in the default browser
Start-Process "http://localhost:19000"