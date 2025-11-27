import { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { useDispatch, useSelector } from "react-redux";
import { userLogin } from "../../redux/slices/DashSlice"; // Assuming DashSlice is correct
import { useNavigate } from "react-router-dom";
import "./SignIn.css";

function SignIn() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const { loginUserStatus: isSuccess, errorOccurred, errMsg } = useSelector((state) => state.user);

  // Use useEffect to handle redirection after successful login
  useEffect(() => {
    if (isSuccess) {
      navigate("/user-dashboard", { replace: true });
    }
  }, [isSuccess, navigate]);

  async function handleFormSubmit(userCred) {
    setIsLoading(true);
    try {
      await dispatch(userLogin(userCred)).unwrap();
    } catch (err) {
      // Error is handled by the rejected case in the slice, which sets the error state.
      console.error("Failed to login:", err);
    }finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="signin-root" style={{ backgroundColor: 'var(--background-color)', color: 'var(--text-color)' }}>
      <div className="signin-container" style={{ backgroundColor: 'var(--container-bg-color)' }}>
        <form className="signin-form" onSubmit={handleSubmit(handleFormSubmit)} style={{ color: 'var(--text-color)' }}>
          <h2>Sign In</h2>
          {errorOccurred && <p className="text-center" style={{ color: 'var(--error-color)' }}>{errMsg}</p>}
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              name="username"
              {...register("username", { required: true })}
              style={{ backgroundColor: 'var(--input-bg-color)', color: 'var(--text-color)', border: '1px solid #999' }}
            />
            {errors.username?.type === "required" && (
              <p style={{ color: 'var(--error-color)' }}>Username is required</p>
            )}
          </div>
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              {...register("password", { required: true })}
              style={{ backgroundColor: 'var(--input-bg-color)', color: 'var(--text-color)', border: '1px solid #999' }}
            />
            {errors.password?.type === "required" && (
              <p style={{ color: 'var(--error-color)' }}>Password is required</p>
            )}
          </div>
          <button type="submit" className="signin-button" disabled={isLoading} style={{ backgroundColor: 'var(--primary-color)', color: '#fff' }}>
            {isLoading ? "Signing In..." : "Sign In"}
          </button>
        </form>
      </div>
    </div>
  );
}

export default SignIn;