def otp_html(otp: str, username: str) -> str:
    return f"""
    <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>OTP Email</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
    }}
    .container {{
      max-width: 400px;
      margin: 0 auto;
      padding: 20px;
      border: 1px solid #ccc;
      border-radius: 8px;
      box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
    }}
    h1 {{
      margin-top: 0;
    }}
    p {{
      margin-bottom: 20px;
    }}
    .otp {{
      background-color: #007bff;
      color: white;
      padding: 10px 20px;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      text-decoration: none;
      display: inline-block;
    }}
    .otp:hover {{
      background-color: #0056b3;
    }}
  </style>
</head>
<body>
  <div class="container">
    <h1>OTP Verification</h1>
    <p>Hello {username}, Your OTP for verification is:</p>
    <h2>{otp}</h2>
    <p>Please use this OTP to verify your account.</p>
    <p>Thank you!</p>
  </div>
</body>
</html>
    """
