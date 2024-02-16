const PatientInfo = () => {
  return (
    <div className="h-full w-full flex flex-row text-slate-200">
      <div className="h-full w-[50%] flex flex-col items-start justify-between">
        <p className="text-3xl font-bold">DOE, JOHN (32 M)</p>
        <div className="text-xl flex flex-col items-start">
          <p>MRN: 0101215</p>
          <p>DOB: 01/02/1992</p>
        </div>
      </div>
      <div className="h-full w-[50%] flex flex-col items-end justify-end">
        <div className="text-xl flex flex-col items-end">
          <p>02 HR 31 MIN ACTIVE</p>
          <p>CONTACT A: (123) 456-7890</p>
          <p>CONTACT B: (123) 456-7890</p>
        </div>
      </div>
    </div>
  );
};

export default PatientInfo;
