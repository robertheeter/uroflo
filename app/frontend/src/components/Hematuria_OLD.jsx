import { useState, useEffect } from "react";
import { IoTriangle } from "react-icons/io5";

const Hematuria = () => {
  const [hematuria, setHematuria] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setHematuria(Math.round(Math.random() * 100));
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div
      className="w-full h-1/3 bg-red-300 rounded-2xl 
                      shadow-xl flex flex-col justify-center items-center gap-1"
    >
      <h1 className="text-3xl font-bold text-slate-900">Hematuria</h1>
      <h1 className="text-2xl text-slate-900">{hematuria}%</h1>
      <div className="w-5/6 h-20 flex justify-center items-center relative">
        <div className="w-full h-10 rounded-lg border-slate-200 border-x-8 border-y-4 flex flex-row">
          <div className="w-1/5 h-full bg-[#ddc588]"></div>
          <div className="w-1/5 h-full bg-[#cf8f70]"></div>
          <div className="w-1/5 h-full bg-[#a8372a]"></div>
          <div className="w-1/5 h-full bg-[#811e1b]"></div>
          <div className="w-1/5 h-full bg-[#491210]"></div>
        </div>

        <div
          className="w-10 h-full absolute transition-all duration-500 -translate-x-1/2 flex flex-col justify-between items-center"
          style={{ left: `${hematuria}%` }}
        >
          <IoTriangle className="text-4xl text-slate-200 rotate-180" />
          <IoTriangle className="text-4xl text-slate-200" />
        </div>
      </div>
    </div>
  );
};

export default Hematuria;
