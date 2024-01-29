const SupplyVolume = () => {
  let currentVolume = 1.2;
  let totalVolume = 3.0;
  let percent = Math.round((currentVolume / totalVolume) * 100);

  return (
    <div
      className="w-[49%] h-full bg-blue-300 rounded-xl 
                       flex flex-row "
    >
      <div className="w-[80%] flex flex-col justify-between items-start px-6 py-1">
        <div className="text-3xl font-bold">SUPPLY VOLUME</div>
        <div className="w-full flex justify-between items-center">
          <div
            className={`w-[125px] h-[48px] font-bold bg-blue-50 flex flex-row justify-center 
        items-center rounded-lg border-black border-4 text-xl`}
          >
            {percent}% FULL
          </div>
          <div className="text-2xl relative -right-5">
            {currentVolume.toFixed(1)}/{totalVolume.toFixed(1)} L
          </div>
        </div>
        <div className="font-bold text-xl">01 HR 32 MIN TO EMPTY</div>
      </div>
      <div className="w-16 flex justify-center items-center">
        <div className="relative w-10 h-24 bg-blue-50 border-black border-2 rounded-sm">
          <div
            className="absolute w-full bottom-0 bg-blue-600 transition-all duration-500"
            style={{ height: `${percent}%` }}
          ></div>
        </div>
      </div>
    </div>
  );
};

export default SupplyVolume;
