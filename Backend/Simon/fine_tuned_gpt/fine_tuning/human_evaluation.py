#%%
from openai import OpenAI
import csv

with open("/Users/simono/Desktop/Thesis/Branches/MediLingo/Backend/Simon/fine_tuned_gpt/fine_tuning/key.txt", 'r') as key:
  API_KEY = key.read()
  
client = OpenAI(api_key=API_KEY)

# id = "ft:gpt-3.5-turbo-0125:personal:medilingo:8z7ujSsh"


# phrase = "Har du nogen form for sukkersyge?"

# completion = client.chat.completions.create(
#   model="ft:gpt-3.5-turbo-0125:personal:medilingo:8z7ujSsh",
#   messages=[
#     {"role": "system", "content": "Translate from danish to ukranian"},
#     {"role": "user", "content": phrase}
#   ]
# )

# print(client.fine_tuning.jobs.retrieve("ftjob-bBZwa98q7ODEm8cMPUPCFLCP").fine_tuned_model)

#print(completion.choices[0].message.content)

# %%
#questions in our test-sample-set for each subdepartment          
     
danish_radiograph_sentences = {
    "MR": 
        ["Har du fået lavet kunstige led?",
        "Har du fået indopereret metal i kroppen?",
        "Er du blevet opereret i et andet land?",
        "Har du nogensinde fået metalsplinter i øjet?",
        "Har du arbejdet som smed, eller andet arbejdet der involverer metalsplinter?",
        "Har du nogen piercinger?",
        "Har du noget metal på dig, for eksempel piercinger?",
        "Har du hårnåle i håret?",
        "Er der nogen mulighed for at du kan være gravid?",
        "Er der en chance for, at du kunne være gravid?",
        "Har du en pacemaker?",
        "Er du hjerteopereret?",
        "Er du blevet opereret i hjertet?",
        "Føler du dig klaustrofobisk i små rum?",
        "Har du oplevet angst i trange eller små rum?",
        "Har du været soldat?",
        "Er du nogensinde blevet ramt af skud eller lignende?",
        "Hvornår fik du indsat din metalprotese?",
        "Har du nogen høreapparater?",
        "Er du nogensinde blevet opereret i hovedet?"],
    "CT": 
        ["Har du nogen kendte allergier?",
        "Har du haft allergiske symptomer tidligere?",
        "Er der noget, du ikke kan tåle på grund af allergi?",
        "Har du haft nogen nyresygdomme?",
        "Er dine nyrer blevet opereret",
        "Har du fået undersøgt din nyrefunktion?",
        "Har du diabetes?",
        "Har du sukkersyge?",
        "Har du fået taget en blodprøve?",
        "Tager du nogen form for medicin?",
        "Har du prøvet at få jod indeholdende kontrast før",
        "Har du nogensinde fået kontrastvæske før?",
        "Skete der noget sidste gang, du fik kontrast",
        "Skete der noget sidste gang, du fik en indsprøjtning med kontrasten?",
        "Du kan opleve en varmefornemmelse i kroppen, når du får kontrastinjektionen",
        "Det kan føles som om, du tisser, når du får kontrasten.",
        "Du kan få en metalsmag i munden af kontrasten",
        "Scanneren vil fortælle dig undervejs, at du skal trække vejret ind og holde det. Efterfølgende vil den også fortælle, når du skal trække vejret normalt igen.",
        "Under scanningen skal du trække vejret ind og holde det i ca. 4-5 sekunder.",
        "Du skal kunne ligge fladt ned på ryggen under hele scanningen"],
    "UL": 
        ["Har du prøvet at få taget en vævsprøve før?",
        "Har du prøvet at få taget en biopsi før?",
        "Er du bange for nåle?",
        "Vi skal tage en vævsprøve fra din lever",
        "Du kommer til at mærke et prik, når vævsprøven bliver taget",
        "Har du prøvet at få lokalbedøvelse før?",
        "Du skal have noget lokalbedøvelse, som bagefter skal have lov til at virke i et minuts tid",
        "Det må ikke gøre ondt, når du har fået lokalbedøvelsen",
        "Du kan mærke at det svier og spænder, når du får lokalbedøvelsen",
        "Efter bedøvelsen skal du ikke kunne mærke noget I det område",
        "Du skal have indsat et kateter i dine lunger",
        "Vi kommer til at hjælpe dig med at kunne trække vejret igen ved at indsætte et kateter i dine lunger",
        "Vi skal indsætte et kateter i dine lunger, så du kan trække vejret bedre",
        "Du kommer til at mærke et lille prik, for vi kan desværre ikke bedøve lungehinden",
        "Lungehinden kan desværre ikke bedøves, så du vil kunne mærke, når vi stikker igennem den",
        "Du har en masse væske i din mave, så vi kommer til at indsætte et dræn for at afhjælpe dig.",
        "Er det muligt at du kan ligge på din venstre side under scanningen?",
        "Det er afgørende, at du ligger stille gennem hele scanningen.",
        "Vi laver undersøgelsen sterilt, så det er meget vigtigt at du ikke rykker eller flytter dig undervejs, når vi stikker dig",
        "Det er vigtigt at du siger til, hvis du får det dårligt."]
}

#correct translated sentence from danish to ukranian
ukranian_radiograph_sentences = {
    "MR":
        ["Чи робили вам штучні суглоби?",
         "Чи вам імплантували метал у тіло хірургічним шляхом?",
         "Вам робили операцію за кордоном?",
         "У вас коли-небудь були металеві уламки в оці",
         "Ви працювали ковалем або на будь-якій іншій роботі, де є ризик ушкодження металевими уламками?",
         "У вас є який-небудь пірсинг?",
         "Чи є на вас який-небудь метал, наприклад, пірсинг?",
         "Ви використовуєте шпильки для волосся?",
         "Чи є можливість того, що ви вагітні?",
         "Чи є ймовірність того, що ви вагітні?",
         "У вас є кардіостимулятор?",
         "Ви перенесли операцію на серці?",
         "Вам робили операцію на серці?",
         "Чи відчуваєте ви клаустрофобію в малих приміщеннях?",
         "Чи відчуваєте ви тривогу в тісному або обмеженому просторі?"
         "Чи ви були солдатом",
         "Чи коли-небудь вас поранено кулею або подібним чином",
         "Коли ви встановили свою металеву протезу?",
         "У вас є які-небудь слухові апарати?",
         "Чи коли-небудь ви проходили операцію на голові?"],
    "CT":
        ["Чи знаєте ви про наявність у вас алергії?",
         "Чи були у вас раніше алергічні симптоми?",
         "Чи є щось, що ви не можете переносити через алергію?",
         "Чи були у вас захворювання нирок?",
         "Чи була у вас коли-небудь операція на нирках?",
         "Чи проходили ви обстеження функції нирок?",
         "У вас був діабет?",
         "Ви хворієте на діабет?",
         "Ви здавали аналіз крові?",
         "Чи приймаєте ви якісь ліки?",
         "Чи намагалися ви раніше вводити контраст, що містить йод?",
         "Чи отримували ви коли-небудь контраст раніше?",
         "Чи сталося щось минулого разу коли вам вводили контраст?",
         "Чи сталося щось під час вашої останньої ін'єкції контрасту?"
         "Ви можете відчувати тепло в тілі під час ін'єкції контрасту",
         "Під час введення контрасту може здаватися, що ви мочитесь.",
         "Ви можете відчути металевий присмак у роті від контрасту.",
         "Сканер буде інформувати вас під час процесу вдиху і затримки дихання, а також коли відновити нормальне дихання.",
         "Під час сканування вам потрібно вдихнути і затримати дихання приблизно на 4-5 секунд.",
         "Ви повинні лежати рівно на спині протягом усього сканування."
        ],
    "UL":
        ["Чи робили вам раніше біопсію тканин?",
         "Чи доводилося вам раніше проходити біопсію тканин?",
         "Чи боїтеся ви голок?",
         "Вам необхідно пройти процедуру взяття зразка тканини з печінки.",
         "Ви відчуєте укол під час взяття зразка тканини.",
         "Ви коли-небудь випробовували місцевий наркоз раніше?",
         "Вам потрібно отримати деякий місцевий наркоз, який потрібно буде дозволити діяти протягом приблизно однієї хвилини.",
         "Це не повинно боліти після того, як ви отримали місцевий наркоз.",
         "При введенні місцевої анестезії ви можете відчути відчуття печіння і стиснення.",
         "Після наркозу ви не повинні відчувати нічого в цій області.",
         "Вам потрібно ввести катетер у легені.",
         "Ми допоможемо вам дихати знову вставивши катетер у ваші легені.",
         "Нам потрібно ввести катетер у ваші легені щоб ви могли краще дихати.",
         "Ви відчуєте невеликий укол тому що на жаль, ми не можемо знеболити плевру.",
         "На жаль, плевру не можна знеболити, тому ви відчуєте укол коли ми будемо її проколювати.",
         "У вас багато рідини в животі, тому ми вставимо дренаж, щоб допомогти вам відчувати полегшення.",
         "Чи можливо, що ви зможете лежати на лівому боці під час сканування?",
         "Дуже важливо щоб ви лежали нерухомо протягом усього сканування.",
         "Ми проводимо обстеження в стерильних умовах, тому дуже важливо, щоб ви не рухалися або не змінювали свого положення, коли ми вас колотимо.",
         "Важливо, щоб ви сказали, якщо ви почуваєте себе погано."
        ]
}

def generate_translations(model_id, path):

    translations = []
    
    for sub_department in danish_radiograph_sentences:
        phrases = danish_radiograph_sentences[sub_department]

        for idx, sentence in enumerate(phrases):
            completion = client.chat.completions.create(
                model=model_id,
                messages=[
                    {"role": "system", "content": "Translate from danish to ukranian"},
                    {"role": "user", "content": sentence}
                ]
            )
            
            generated_translation = completion.choices[0].message.content #generated translated sentence
            translations.append(f"{sentence} : {generated_translation}")
        
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['danish', 'generated_translation'])
        for sentence in translations:
            danish, generated_translation = sentence.split(":")
            writer.writerow([danish.strip(), generated_translation.strip()])

# %%



# %%