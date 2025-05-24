import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const Test = () => {
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const message = queryParams.get('message');

    return (
    <div>
      <h1>{message}</h1>
    </div>
  );
};

export default Test;