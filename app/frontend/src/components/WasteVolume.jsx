import { useEffect, useState } from "react";
import axios from "axios";

const WasteVolume = () => {
  let [volume, setVolume] = useState(0);

  useEffect(() => {
    const intervalId = setInterval(() => {
      axios
        .get("http://localhost:8000/interface/api/device") // replace with your API endpoint
        .then((response) => setVolume(response.data.waste_volume)) // replace 'rate' with the actual key in the response
        .catch((error) => console.error(error));
    }, 1000); // fetch every 1 second

    return () => clearInterval(intervalId); // clean up on component unmount
  }, []);

  volume = volume / 1000;
  let totalVolume = 5.0;
  let percent = Math.round((volume / totalVolume) * 100);

  const [time, setTime] = useState(0);

  useEffect(() => {
    const intervalId = setInterval(() => {
      axios
        .get("http://localhost:8000/interface/api/device") // replace with your API endpoint
        .then((response) => setTime(response.data.waste_time)) // replace 'rate' with the actual key in the response
        .catch((error) => console.error(error));
    }, 1000); // fetch every 1 second

    return () => clearInterval(intervalId); // clean up on component unmount
  }, []);

  let hours = Math.floor(time / 60);
  let minutes = time % 60;

  return (
    <div
      className="w-[48.5%] h-full bg-slate-900 rounded-xl
                       flex flex-row "
    >
      <div className="w-[95%] flex flex-col justify-between items-start px-4 py-3">
        <div className="text-2xl text-slate-200">WASTE VOLUME</div>
        <div className="w-full flex justify-between items-center">
          <div
            className={`h-[40px] font-bold bg-slate-200 flex flex-row justify-left 
        items-center rounded-lg text-2xl text-slate-950 px-3`}
          >
            {percent}% FULL
          </div>
          <div className="text-2xl text-slate-200 relative -right-3">
            {volume.toFixed(1)}/{totalVolume.toFixed(1)} L
          </div>
        </div>
        <div className="text-lg text-slate-200">
          {hours} HR {minutes} MIN TO FULL
        </div>
      </div>
      <div className="w-16 flex justify-center items-center">
        <div className="relative w-5 h-24 bg-slate-200 rounded-2xl">
          <div
            className="absolute w-full bottom-0 bg-yellow-500 transition-all duration-500 rounded-2xl"
            style={{ height: `${percent}%` }}
          ></div>
        </div>
      </div>
    </div>
  );
};

export default WasteVolume;
