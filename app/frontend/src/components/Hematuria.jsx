import { IoTriangle } from "react-icons/io5";

const Hematuria = () => {
  const text = "MILD"; // Change this value to "CLEAR", "MILD", "MODERATE", or "SEVERE"

  let textSize;
  if (text === "CLEAR") {
    textSize = "text-3xl";
  } else if (text === "MILD") {
    textSize = "text-4xl";
  } else if (text === "MODERATE") {
    textSize = "text-xl";
  } else if (text === "SEVERE") {
    textSize = "text-3xl";
  } else {
    textSize = "text-base";
  }

  return (
    <div
      className="w-[750px] h-[136px] bg-red-300 rounded-xl 
                       flex flex-col justify-center items-center"
    >
      <div className="w-full flex justify-center gap-x-52">
        <div className="text-3xl font-bold text-slate-900">
          HEMATURIA SEVERITY
        </div>
        <div className="text-3xl text-slate-900">{50}% BLOOD</div>
      </div>
      <div className="w-full flex justify-center gap-5 items-center">
        <div
          className={`w-1/6 h-2/3 font-bold bg-red-50 flex justify-center items-center rounded-md border-black border-4 ${textSize}`}
        >
          {text}
        </div>
        <div className="w-3/4 h-20 flex flex-col justify-center items-center relative">
          <div className="w-full h-10 rounded-lg bg-slate-200 border-slate-200 border-[6px] flex flex-row">
            <div className="w-1/4 h-full bg-[#ddc588] text-xl relative flex justify-center items-center rounded-l-md">
              <p className="absolute -bottom-8 font-bold">CLEAR</p>
            </div>
            <div className="w-1/4 h-full bg-[#cf8f70] text-xl relative flex justify-center items-center">
              <p className="absolute -bottom-8 font-bold">MILD</p>
            </div>
            <div className="w-1/4 h-full bg-[#a8372a] text-xl relative flex justify-center items-center">
              <p className="absolute -bottom-8 font-bold">MODERATE</p>
            </div>
            <div className="w-1/4 h-full bg-[#491210] text-xl relative flex justify-center items-center">
              <p className="absolute -bottom-8 font-bold">SEVERE</p>
            </div>
          </div>

          <div
            className="w-10 h-5/6 absolute transition-all duration-500 -translate-x-1/2 flex flex-col justify-between items-center"
            style={{ left: `50%` }}
          >
            <IoTriangle className="text-3xl text-slate-200 rotate-180" />
            <IoTriangle className="text-3xl text-slate-200" />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Hematuria;
