import React, { useState } from "react"; // ✅ دمج الاستيراد
import { useLocation, useNavigate } from "react-router-dom";
import axios from "axios";
import { useAuth } from "../AuthContext";

const OtpInput = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [otp, setOtp] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();

  const email = location.state ? location.state.email : "";

  const handleOtpVerification = () => {
    setLoading(true);
    setError(null);

    axios
      .post("http://127.0.0.1:8000/auth/verify-otp", {
        email,
        otp,
      })
      .then((res) => {
        console.log(res.data);
        login(res.data.user);

        // ✅ حفظ التوكن في LocalStorage
        localStorage.setItem("token", res.data.token);

        // ✅ بعد الحفظ انتقل إلى الصفحة الرئيسية
        navigate("/home");
      })
      .catch((err) => {
        console.log(err);
        setError("Invalid OTP. Please check the OTP you entered.");
      })
      .finally(() => {
        setLoading(false);
      });
  };

  return (
    <div className="App">
      <div className="otp-container">
        <h1>Enter OTP</h1>
        {email && (
          <h3>
            OTP has been sent to your email: {email}. Please enter the OTP below
            to access your account.
          </h3>
        )}

        <input
          type="text"
          placeholder="Enter OTP"
          value={otp}
          onChange={(e) => setOtp(e.target.value)}
        />
        <input type="email" placeholder="Email" value={email} readOnly />
        <button onClick={handleOtpVerification} disabled={loading}>
          {loading ? "Verifying..." : "Verify OTP"}
        </button>

        {error && <div className="error">{error}</div>}
      </div>
    </div>
  );
};

export default OtpInput;
