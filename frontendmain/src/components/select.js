import React from "react";

export const Select = ({ children, ...props }) => {
  return (
    <select
      className="w-full p-2 border border-gray-300 rounded-lg"
      {...props}
    >
      {children}
    </select>
  );
};
