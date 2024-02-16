import SupplyVolume from "./SupplyVolume";
import WasteVolume from "./WasteVolume";

const Volume = () => {
  return (
    <div className="w-full h-[162px] flex flex-row justify-between items-center">
      <SupplyVolume />
      <WasteVolume />
    </div>
  );
};

export default Volume;
