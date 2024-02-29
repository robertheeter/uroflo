import axios from "axios";
import { useEffect, useState } from "react";

const WasteVolume = () => {
  let [volume, setVolume] = useState(0);
  let [totalVolume, setTotalVolume] = useState(1);

  useEffect(() => {
    const intervalId = setInterval(() => {
      axios
        .get("http://localhost:8000/system") // replace with your API endpoint
        .then((response) => setTotalVolume(response.data.waste_volume_total)) // replace 'rate' with the actual key in the response
        .catch((error) => console.error(error));
    }, 1000); // fetch every 1 second

    return () => clearInterval(intervalId); // clean up on component unmount
  }, []);

  useEffect(() => {
    const intervalId = setInterval(() => {
      axios
        .get("http://localhost:8000/system") // replace with your API endpoint
        .then((response) => setVolume(response.data.waste_volume)) // replace 'rate' with the actual key in the response
        .catch((error) => console.error(error));
    }, 1000); // fetch every 1 second

    return () => clearInterval(intervalId); // clean up on component unmount
  }, []);

  volume = volume / 1000;
  totalVolume = totalVolume / 1000;
  let percent = Math.round((volume / totalVolume) * 100);

  const [time, setTime] = useState(0);

  useEffect(() => {
    const intervalId = setInterval(() => {
      axios
        .get("http://localhost:8000/system") // replace with your API endpoint
        .then((response) => setTime(response.data.waste_time)) // replace 'rate' with the actual key in the response
        .catch((error) => console.error(error));
    }, 1000); // fetch every 1 second

    return () => clearInterval(intervalId); // clean up on component unmount
  }, []);

  let hours = Math.floor(time / 60);
  let minutes = time % 60;

  return (
    <div
      className="w-[48.5%] h-full bg-slate-900 rounded-2xl
                       flex flex-row "
    >
      <div className="w-[95%] flex flex-col justify-between items-start px-5 py-4">
        <div className="text-3xl text-slate-200">WASTE VOLUME</div>
        <div className="w-full flex justify-between items-center mt-1 mb-1">
          <div
            className={`font-bold bg-slate-200 flex flex-row justify-left 
        items-center rounded-lg text-3xl text-slate-950 px-3 py-1`}
          >
            {Math.min(Math.max(percent, 0), 100)}% FULL
          </div>
          <div className="text-3xl text-slate-200 relative -right-3">
            {volume.toFixed(1)}/{totalVolume.toFixed(1)} L
          </div>
        </div>
        <div className="text-xl text-slate-200">
          {hours} h {minutes} min TO FULL
        </div>
      </div>
      <div className="w-16 flex justify-center items-center">
        <div className="relative w-6 h-28 mr-2 bg-slate-200 rounded-2xl">
          <div
            className="absolute w-full bottom-0 bg-yellow-500 transition-all duration-500 rounded-2xl"
            style={{ height: `${Math.min(percent, 100)}%` }}
          ></div>
        </div>
      </div>
    </div>
  );
};

export default WasteVolume;
