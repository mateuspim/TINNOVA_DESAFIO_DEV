function LoadingStatus({ what }) {
  return (
    <div className="loading-container">
      <h2>Loading Content</h2>

      <div className="loading-animation">
        <div className="spinner"></div>
      </div>

      <p className="loading-info">
        Please wait while your {what} is loading...
      </p>
    </div>
  );
}

export default LoadingStatus;