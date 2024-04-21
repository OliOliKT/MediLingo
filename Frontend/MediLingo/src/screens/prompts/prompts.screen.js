import React from "react";
import { FlatList } from "react-native";
import { useAppContext } from '../../components/context';
import { useNavigation } from '@react-navigation/native'; 
import { TouchableOpacity } from 'react-native';
import {
    PhrasesContent,   
    ItemSeparator,
    PhraseDetails,
    Phrase,
    SafeArea,
    Headline
  } from "./prompts.styles";

const departmentNameMapping = { 
    ctScanning: "CT-scanning",
    mriScanning: "MR-scanning",
    ultrasound: "Ultralyd"

};

const prompts = {
    categories: {
        general: { title: "Generelle spørgsmål" },
        allergies: { title: "Allergier" },
        metal: { title: "Metal" },
        kidney: { title: "Nyre" },
        diabetes: { title: "Diabetes" },
        kontrast: { title: "Kontrast" },
        claustrophobia: { title: "Klaustrofobi" },
        sedation: { title: "Bedøvelse" },
        cathether: { title: "Kateter" },
        pregnancy: { title: "Graviditet" },
        biopsi: { title: "Biopsi" },
        ctScanning: { title: "CT-scanning" },
        mriScanning: { title: "MR-scanning" },
        ultrasound: { title: "Ultralyd" },
    },
    departments: {
        ctScanning: ["general", "allergies", "kidney", "diabetes", "kontrast", "ctScanning"],
        mriScanning: ["general", "metal", "claustrophobia", "pregnancy", "mriScanning"],
        ultrasound: ["general", "biopsi", "sedation", "cathether",  "ultrasound"],
    },
    general: [
        "Hvad er dit fulde navn?",
        "Hvad er dit cpr-nummer?",
        "Hvad er din fødselsdato?",
        "Hvad er din adresse?",
        "Hvad er dit telefonnummer?",
        "Hvad er din e-mail?",
        "Hvad er din læges navn?",
    ],
    biopsi: [
        "Har du prøvet at få taget en vævsprøve før?",
        "Har du prøvet at få taget en biopsi før?",
        "Er du bange for nåle?",
        "Vi skal tage en vævsprøve fra din lever.",
        "Du kommer til at mærke et prik, når vævsprøven bliver taget.",
    ],
    allergies: [
        "Har du nogen kendte allergier?",
        "Har du haft allergiske symptomer tidligere?",
        "Er der noget, du ikke kan tåle på grund af allergi?",
    ],
    pregnancy: [
        "Er der en chance for, at du kunne være gravid?",
        "Er der nogen mulighed for at du kan være gravid?",
    ],
    metal: [
        "Har du fået lavet kunstige led?",
        "Har du fået indopereret metal i kroppen?",
        "Er du blevet opereret i et andet land?",
        "Har du nogensinde fået metalsplinter i øjet?",
        "Har du arbejdet som smed, eller andet arbejdet der involverer metalsplinter?",
        "Har du nogen piercinger?",
        "Har du noget metal på dig, for eksempel piercinger?",
        "Har du hårnåle i håret?",
        "Har du været soldat?",
        "Er du nogensinde blevet ramt af skud eller lignende?",
        "Hvornår fik du indsat din metalprotese?",
        "Har du nogen høreapparater?",
    ],
    kidney: [
        "Har du haft nogen nyresygdomme?",
        "Er dine nyrer blevet opereret?",
        "Har du fået undersøgt din nyrefunktion?",
    ],
    diabetes: [
        "Har du diabetes?",
        "Har du sukkersyge?",
    ],
    kontrast: [
        "Har du nogensinde fået kontrastvæske før?",
        "Skete der noget sidste gang, du fik en indsprøjtning med kontrasten?",
        "Du kan opleve en varmefornemmelse i kroppen, når du får kontrastinjektionen.",
        "Det kan føles som om, du tisser, når du får kontrasten.",
        "Du kan få en metalsmag i munden af kontrasten.",
        "Har du prøvet at få jodholdig kontrast før?",
    ],
    claustrophobia: [
        "Føler du dig klaustrofobisk i små rum?",
        "Har du oplevet angst i trange eller små rum?",
    ],
    sedation: [
        "Har du prøvet at få lokalbedøvelse før?",
        "Du skal have noget lokalbedøvelse, som bagefter skal have lov til at virke i et minuts tid.",
        "Det må ikke gøre ondt, når du har fået lokalbedøvelsen.",
        "Du kan mærke at det svier og spænder, når du får lokalbedøvelsen.",
        "Efter bedøvelsen skal du ikke kunne mærke noget I det område.",
    ],
    cathether: [
        "Du skal have indsat et kateter i dine lunger.",
        "Vi kommer til at hjælpe dig med at kunne trække vejret igen ved at indsætte et kateter i dine lunger.",
        "Vi skal indsætte et kateter i dine lunger, så du kan trække vejret bedre.",
    ],
    ctScanning: [
        "Har du fået taget en blodprøve?",
        "Tager du nogen form for medicin?",
        "Scanneren vil fortælle dig undervejs, at du skal trække vejret ind og holde det. Efterfølgende vil den også fortælle, når du skal trække vejret normalt igen.",
        "Under scanningen skal du trække vejret ind og holde det i ca. 4-5 sekunder.",
        "Du skal kunne ligge fladt ned på ryggen under hele scanningen."
    ],
    mriScanning: [
        "Har du en pacemaker?",
        "Er du hjerteopereret?",
        "Er du blevet opereret i hjertet?",
        "Er du nogensinde blevet opereret i hovedet?"],
    ultrasound: [
        "Du kommer til at mærke et lille prik, for vi kan desværre ikke bedøve lungehinden.",
        "Lungehinden kan desværre ikke bedøves, så du vil kunne mærke, når vi stikker igennem den",
        "Du har en masse væske i din mave, så vi kommer til at indsætte et dræn for at afhjælpe dig.",
        "Er det muligt at du kan ligge på din venstre side under scanningen?",
        "Det er afgørende, at du ligger stille gennem hele scanningen.",
        "Vi laver undersøgelsen sterilt, så det er meget vigtigt at du ikke rykker eller flytter dig undervejs, når vi stikker dig",
        "Det er vigtigt at du siger til, hvis du får det dårligt."]
};

const PhraseItem = React.memo(({ item }) => {
    
    return (
        <PhrasesContent>
            <PhraseDetails>
                <Phrase>{item}</Phrase>
            </PhraseDetails>
        </PhrasesContent>
    );
    });


export const PromptsScreen = () => {
    const { selectedDepartment, updateSelectedPhrase } = useAppContext();
    const navigation = useNavigation(); 

    const handlePressItem = (phrase) => {
        updateSelectedPhrase(phrase, true);
        navigation.navigate('Oversæt');
    };

    const renderItem = ({ item }) => (
        <TouchableOpacity onPress={() => handlePressItem(item)}>
            <PhraseItem item={item} />
        </TouchableOpacity>
    );

    const departmentCategories = prompts.departments[selectedDepartment];
    const departmentPrompts = departmentCategories.map(category => ({
        title: prompts.categories[category].title,
        data: prompts[category].slice().sort((a, b) => a.localeCompare(b))
    }));
    
    return (
        <SafeArea>
            <FlatList
                ListHeaderComponent={
                    <Headline>Spørgsmål &#40;{departmentNameMapping[selectedDepartment]}&#41;:</Headline>
                }
                data={departmentPrompts}
                keyExtractor={(item, index) => `${item.title}-${index}`}
                renderItem={({ item }) => (
                    <>
                        <Headline>{item.title}</Headline>
                        <FlatList
                            data={item.data}
                            keyExtractor={(_, i) => String(i)}
                            renderItem={renderItem}
                            ItemSeparatorComponent={ItemSeparator}
                        />
                    </>
                )}
                ItemSeparatorComponent={ItemSeparator}
            />
        </SafeArea>
    );
}