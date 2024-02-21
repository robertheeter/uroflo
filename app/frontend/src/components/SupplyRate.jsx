import axios from "axios";
import { useEffect, useState } from "react";

const SupplyRate = () => {
  const [rate, setRate] = useState(0);

  useEffect(() => {
    const intervalId = setInterval(() => {
      axios
        .get("http://localhost:8000/system") // replace with your API endpoint
        .then((response) => setRate(response.data.supply_rate)) // replace 'rate' with the actual key in the response
        .catch((error) => console.error(error));
    }, 1000); // fetch every 1 second

    return () => clearInterval(intervalId); // clean up on component unmount
  }, []);

  return (
    <div
      className="w-[48.5%] h-full bg-slate-900 rounded-2xl 
                       flex flex-row "
    >
      <div className="w-full h-full flex flex-col justify-between items-start px-5 py-4">
        <div className="text-3xl text-slate-200">SUPPLY INFLOW</div>
        <div className="w-full flex flex-col justify-center items-center mb-20">
          <div className="font-bold text-slate-200 text-3xl mb-[9px]">
            {rate} mL/min
          </div>
          <div className="w-full h-6 rounded-2xl bg-slate-200">
            <div
              className="h-full bg-blue-500 rounded-2xl transition-all duration-500"
              style={{ width: `${rate}%` }}
            ></div>
            <div className="flex flex-row justify-between items-center">
              <div className="text-xl text-slate-200">0</div>
              <div className="text-xl text-slate-200">100</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SupplyRate;
