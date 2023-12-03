import axios from "axios";
import {
  useState,
  useEffect
} from "react";
import {
  ChakraProvider,
  Progress,
  Flex,
  Box,
  Text,
  Spacer,
  Image,
} from "@chakra-ui/react";


function App() {
  axios.defaults.baseURL = "http://localhost:8000"; // proxy

  const [hematuria_level, setHematuriaLevel] = useState(0); // integer; outflow hematuria level/severity
  // const [hematuria_color, setHematuriaColor] = useState([]); // outflow 0-255 [R, G, B] color

  const [supply_volume, setSupplyVolume] = useState(0); // float (mL); supply bag volume
  const [supply_rate, setSupplyRate] = useState(0); // float (mL/min); supply bag flow rate
  const [supply_percent, setSupplyPercent] = useState(0); // float (%); percent supply bag full
  const [supply_time, setSupplyTime] = useState(0); // integer (s); time to supply bag empty

  // const [waste_volume, setWasteVolume] = useState(0); // float (mL); waste bag volume
  // const [waste_rate, setWasteRate] = useState(0); // float (mL/min); waste bag flow rate
  // const [waste_percent, setWastePercent] = useState(0); // float (%); percent waste bag full
  // const [waste_time, setWasteTime] = useState(0);  // integer (s); time to waste bag full

  // const [occlusion_level, setOcclusionLevel] = useState(0); // integer; peristaltic pump or tube compression occlusion level
  
  // const [device_status, setDeviceStatus] = useState(0); // integer; CBI notification status
  // const [device_mode, setDeviceMode] = useState(0); // boolean; automatic or manual device control mode

  // const [patient_first_name, setPatientFirstName] = useState(0); // string; patient first name
  // const [patient_middle_name, setPatientMiddleName] = useState(0); // string; patient middle name
  // const [patient_last_name, setPatientLastName] = useState(0); // string; patient last name
  // const [patient_id, setPatientId] = useState(0); // string; patient ID
  // const [patient_birth_date, setPatientBirthDate] = useState(0); // date; patient date of birth

  // const [doctor_first_name, setDoctorFirstName] = useState(0); // string; doctor first name
  // const [doctor_middle_name, setDoctorMiddleName] = useState(0); // string; doctor middle name
  // const [doctor_last_name, setDoctorLastName] = useState(0); // string; doctor last name
  // const [doctor_id, setDoctorId] = useState(0); // string; doctor ID

  // const [duration_time, setDurationTime] = useState(0); // integer (min); duration on CBI
 

  const [time, setTime] = useState(
    new Date().toLocaleString("en-US", {
      hour: "2-digit",
      minute: "2-digit",
      month: "2-digit",
      day: "2-digit",
      year: "numeric",
      hour12: true,
    })
  );

  useEffect(() => {
    const interval = setInterval(() => {
      axios
        .get("http://localhost:8000/user_interface/get_hematuria")
        .then((response) => {
          setHematuriaLevel(response.data.level);
          // setHematuriaColor(response.data.color);
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
        });
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      axios
        .get("http://localhost:8000/user_interface/get_supply")
        .then((response) => {
          setSupplyVolume(response.data.volume);
          setSupplyRate(response.data.rate);
          setSupplyPercent(response.data.percent);
          setSupplyTime(response.data.time);
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
        });
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const timer = setInterval(() => {
      setTime(
        new Date().toLocaleString("en-US", {
          hour: "2-digit",
          minute: "2-digit",
          month: "2-digit",
          day: "2-digit",
          year: "numeric",
          hour12: true,
        })
      );
    }, 1000);

    return () => {
      clearInterval(timer);
    };
  }, []);

  const getColor = (value) => {
    if (value <= 20) {
      return "#ddc588";
    } else if (value <= 40) {
      return "#cf8f70";
    } else if (value <= 60) {
      return "#a8372a";
    } else if (value <= 80) {
      return "#811e1b";
    } else {
      return "#491210";
    }
  };

  return (
    <ChakraProvider>
      <Flex direction="column" h="100vh">
        <Flex
          as="header"
          width="100%"
          padding="1rem"
          boxShadow="md"
          justifyContent="space-between"
          alignItems="center"
        >
          <Image
            src="uroflo_logo_full.png"
            alt="Description of the image"
            boxSize="100px"
            objectFit="contain"
          />
          <Text fontSize="2xl" fontWeight="bold">
            {time}
          </Text>
        </Flex>
        <Flex direction="row" h="100vh">
          <Flex direction="column" flex="1" align="center" justify="center">
            <Text fontSize="5xl" fontWeight="bold" marginTop="3">
              Doe, John
            </Text>
            <Text fontSize="xl" fontWeight="bold" marginTop="3">
              Patient ID: 123456789
            </Text>
            <Text fontSize="xl" fontWeight="bold" marginTop="3">
              DOB: 01/01/1990
            </Text>
          </Flex>

          <Flex direction="column" flex="3">
            <Flex direction="column" justify="center" align="center" flex="1">
              <Box
                display="flex"
                flexDirection="column"
                alignItems="center"
                justifyContent="center"
                textAlign="center"
                width="75%"
                borderRadius="30px"
                padding="6"
                background="#fceded"
              >
                <Text fontSize="3xl" fontWeight="bold" marginBottom="1">
                  Hematuria Degree
                </Text>

                <Box marginBottom="4">
                  <Text fontSize="2xl">{hematuria}%</Text>
                </Box>

                <Spacer />

                <Progress
                  value={hematuria}
                  width="80%"
                  borderRadius="full"
                  bgColor="white"
                  sx={{
                    div: {
                      backgroundColor: getColor(hematuria),
                    },
                    "& > div:first-child": {
                      transitionProperty: "width",
                    },
                  }}
                />
              </Box>
            </Flex>

            <Flex direction="column" justify="center" align="center" flex="1">
              <Box
                display="flex"
                flexDirection="column"
                alignItems="center"
                justifyContent="center"
                textAlign="center"
                width="75%"
                borderRadius="30px"
                padding="6"
                background="#e1effa"
              >
                <Text fontSize="3xl" fontWeight="bold" marginBottom="1">
                  Saline Weight
                </Text>

                <Box marginBottom="4">
                  <Text fontSize="2xl">{saline} L</Text>
                  <Text fontSize="2xl">{salinepercent}% Left</Text>
                </Box>

                <Spacer />

                <Progress
                  value={saline}
                  width="80%"
                  borderRadius="full"
                  bgColor="white"
                  colorScheme="blue"
                  sx={{
                    "& > div:first-child": {
                      transitionProperty: "width",
                    },
                  }}
                />
              </Box>
            </Flex>
          </Flex>
        </Flex>
      </Flex>
    </ChakraProvider>
  );
}

export default App;
