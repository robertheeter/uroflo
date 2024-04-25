import { useState, useEffect } from "react";
import UroFloLogo from "../assets/uroflo_blue_name_cropped.svg";

const Time = () => {
  const [currentDateTime, setCurrentDateTime] = useState(new Date());

  useEffect(() => {
    const intervalId = setInterval(() => {
      setCurrentDateTime(new Date());
    }, 1000);

    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className="h-full w-full flex flex-col justify-end items-end text-xl gap-y-2">
      <img src={UroFloLogo} alt="Description of Image" className="w-[65%]" />
      <div className="text-xl flex flex-col items-end">
        <p>
          4/24/2024 23:42
        </p>
      </div>
    </div>
  );
};

export default Time;
