import WasteVolume from "./WasteVolume";
import WasteRate from "./WasteRate";

const Waste = () => {
  return (
    <div className="w-full h-[162px] flex flex-row justify-between items-center">
      <WasteVolume />
      <WasteRate />
    </div>
  );
};

export default Waste;
