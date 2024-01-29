import SupplyVolume from "./SupplyVolume";
import SupplyRate from "./SupplyRate";

const Supply = () => {
  return (
    <div className="w-[750px] h-[136px] flex flex-row justify-between items-center">
      <SupplyVolume />
      <SupplyRate />
    </div>
  );
};

export default Supply;
