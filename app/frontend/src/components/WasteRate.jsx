import { useEffect, useState } from "react";
import axios from "axios";

const WasteRate = () => {
  //  let rate = 63; // Change this value to a number between 0 and 100
  const [rate, setRate] = useState(0);

  useEffect(() => {
    const intervalId = setInterval(() => {
      axios
        .get("http://localhost:8000/interface/api/device") // replace with your API endpoint
        .then((response) => setRate(response.data.waste_rate)) // replace 'rate' with the actual key in the response
        .catch((error) => console.error(error));
    }, 1000); // fetch every 1 second

    return () => clearInterval(intervalId); // clean up on component unmount
  }, []);

  return (
    <div
      className="w-[48.5%] h-full bg-slate-900 rounded-xl 
                       flex flex-row "
    >
      <div className="w-full h-full flex flex-col justify-between items-start px-4 py-3">
        <div className="text-2xl text-slate-200">WASTE OUTFLOW</div>
        <div className="w-full flex flex-col justify-center items-center mb-20">
          <div className="font-bold text-slate-200 text-2xl pb-1">
            {rate} mL/min
          </div>
          <div className="w-full h-5 rounded-2xl bg-slate-200">
            <div
              className="h-full bg-yellow-500 rounded-2xl transition-all duration-500"
              style={{ width: `${rate}%` }}
            ></div>
            <div className="flex flex-row justify-between items-center">
              <div className="text-lg text-slate-200">0</div>
              <div className="text-lg text-slate-200">100</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WasteRate;
