import React from "react";
import { SectionList } from "react-native";
import { useAppContext } from "../../components/context";
import { useNavigation } from "@react-navigation/native";
import { TouchableOpacity } from "react-native";
import {
  PhrasesContent,
  ItemSeparator,
  PhraseDetails,
  Phrase,
  SafeArea,
  Headline,
  SectionHeader,
} from "./prompts.styles";

const departmentNameMapping = {
  ctScanning: "CT-scanning",
  mriScanning: "MR-scanning",
  ultrasound: "Ultralyd",
};

// Define all categories and their questions
const categories = {
  "Generelle spørgsmål": [
    "Har du nogen kendte allergier?",
    "Har du haft allergiske symptomer tidligere?",
    "Er der noget, du ikke kan tåle på grund af allergi?",
    "Har du diabetes?",
    "Har du sukkersyge?",
    "Tager du nogen form for medicin?",
    "Har du prøvet at få jodholdig kontrast før?",
    "Har du nogensinde fået kontrastvæske før?",
  ],
  "Nyresygdomme": [
    "Har du haft nogen nyresygdomme?",
    "Er dine nyrer blevet opereret?",
    "Har du fået undersøgt din nyrefunktion?",
  ],
  "Info om scanning": [
    "Scanneren vil fortælle dig undervejs, at du skal trække vejret ind og holde det.",
    "Under scanningen skal du trække vejret ind og holde det i ca. 4-5 sekunder.",
    "Du skal kunne ligge fladt ned på ryggen under hele scanningen.",
  ],
  "Metal i kroppen": [
    "Har du fået lavet kunstige led?",
    "Har du fået indopereret metal i kroppen?",
    "Har du nogensinde fået metalsplinter i øjet?",
    "Har du arbejdet som smed, eller andet arbejdet der involverer metalsplinter?",
    "Har du nogen piercinger?",
    "Har du noget metal på dig, for eksempel piercinger?",
    "Har du hårnåle i håret?",
    "Hvornår fik du indsat din metalprotese?",
  ],
  "Andre spørgsmål": [
    "Er der nogen mulighed for at du kan være gravid?",
    "Har du en pacemaker?",
    "Er du hjerteopereret?",
    "Føler du dig klaustrofobisk i små rum?",
    "Har du oplevet angst i trange eller små rum?",
  ],
  "Biopsi og bedøvelse": [
    "Har du prøvet at få taget en vævsprøve før?",
    "Har du prøvet at få lokalbedøvelse før?",
    "Du skal have noget lokalbedøvelse, som bagefter skal have lov til at virke i et minuts tid.",
    "Det må ikke gøre ondt, når du har fået lokalbedøvelsen.",
    "Du kan mærke at det svier og spænder, når du får lokalbedøvelsen.",
  ],
  "Dræn og kateter": [
    "Du skal have indsat et kateter i dine lunger.",
    "Vi skal indsætte et kateter i dine lunger, så du kan trække vejret bedre.",
    "Du har en masse væske i din mave, så vi kommer til at indsætte et dræn for at afhjælpe dig.",
  ],
};

// Map departments to the categories they should display
const departmentCategories = {
  ctScanning: ["Generelle spørgsmål", "Nyresygdomme", "Info om scanning", "Andre spørgsmål"],
  mriScanning: ["Generelle spørgsmål", "Metal i kroppen", "Andre spørgsmål"],
  ultrasound: ["Generelle spørgsmål", "Biopsi og bedøvelse", "Dræn og kateter", "Andre spørgsmål"],
};

const PhraseItem = React.memo(({ item, onPress }) => (
  <TouchableOpacity onPress={() => onPress(item)}>
    <PhrasesContent>
      <PhraseDetails>
        <Phrase>{item}</Phrase>
      </PhraseDetails>
    </PhrasesContent>
  </TouchableOpacity>
));

export const PromptsScreen = () => {
  const { selectedDepartment, updateSelectedPhrase } = useAppContext();
  const navigation = useNavigation();

  const handlePressItem = (phrase) => {
    updateSelectedPhrase(phrase, true);
    navigation.navigate("Oversæt");
  };

  const sections = React.useMemo(() => {
    const departmentCategoryKeys = departmentCategories[selectedDepartment] || [];
    return departmentCategoryKeys.map((category) => ({
      title: category,
      data: categories[category],
    }));
  }, [selectedDepartment]);

  return (
    <SafeArea>
      <Headline>Spørgsmål ({departmentNameMapping[selectedDepartment]}):</Headline>
      <SectionList
        sections={sections}
        keyExtractor={(item, index) => index.toString()}
        renderItem={({ item }) => (
          <PhraseItem item={item} onPress={handlePressItem} />
        )}
        renderSectionHeader={({ section: { title } }) => (
          <SectionHeader>{title}:</SectionHeader>
        )}
        ItemSeparatorComponent={ItemSeparator}
      />
    </SafeArea>
  );
};