import WasteVolume from "./WasteVolume";
import WasteRate from "./WasteRate";

const Waste = () => {
  return (
    <div className="w-[750px] h-[136px] flex flex-row justify-between items-center">
      <WasteVolume />
      <WasteRate />
    </div>
  );
};

export default Waste;
