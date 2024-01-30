const WasteRate = () => {
  let rate = 30; // Change this value to a number between 0 and 100

  return (
    <div
      className="w-[48.5%] h-full bg-amber-200 rounded-xl 
                       flex flex-row "
    >
      <div className="w-full h-full flex flex-col justify-between items-start px-6 py-1">
        <div className="text-2xl font-bold">WASTE INFLOW</div>
        <div className="w-full flex flex-col justify-center items-center pb-8">
          <div className="font-bold text-2xl pb-1">{rate} mL/min</div>
          <div className="w-full h-5 rounded-3xl bg-yellow-50">
            <div
              className="h-full bg-yellow-500 rounded-3xl transition-all duration-500"
              style={{ width: `${rate}%` }}
            ></div>
            <div className="flex flex-row justify-between items-center">
              <div className="text-2xl">0</div>
              <div className="text-2xl">100</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WasteRate;
