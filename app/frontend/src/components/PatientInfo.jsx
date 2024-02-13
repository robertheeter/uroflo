const PatientInfo = () => {
  return (
    <div className="h-full w-full flex flex-row text-slate-200">
      <div className="h-full w-1/2 flex flex-col items-start justify-between">
        <p className="text-3xl font-bold">DOE, JOHN (32 M)</p>
        <div className="text-xl flex flex-col items-start">
          <p>MRN: 0101215</p>
          <p>DOB: 01/02/1992</p>
        </div>
      </div>
      <div className="h-full w-1/2 flex flex-col items-end justify-between">
        <p className="text-3xl font-bold">02 HR 05 MIN ON CBI</p>
        <div className="text-xl flex flex-col items-end">
          <p>09:12</p>
          <p>02/12/2024</p>
        </div>
      </div>
    </div>
  );
};

export default PatientInfo;
