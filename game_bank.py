from chapter_guides import GITA
from quiz import QUESTIONS as OLD
from knowledge import CONTENT
# Each entry is authored from the referenced episode. Variants test different skills.
CHARACTERS=[
('Sudama','He visits an old school friend with a modest food gift.','He is reluctant to present the flattened rice.','Bhagavatam 10.80–81'),
('Dhruva','A painful family encounter sends this child in search of lasting honour.','Narada guides his forest practice.','Bhagavatam 4.8–9'),
('Suniti','She responds to her child’s hurt without encouraging revenge.','She is Dhruva’s mother.','Bhagavatam 4.8'),
('Suruchi','Her words in a royal household deeply hurt a young child.','She is Uttama’s mother, not Dhruva’s mother.','Bhagavatam 4.8'),
('Uttanapada','A conflict in his household begins Dhruva’s journey.','He is the father of Dhruva and Uttama.','Bhagavatam 4.8'),
('Narada','He listens to a determined child and teaches a way of practice.','He guides Dhruva and also tells Vyasa about his own earlier life.','Bhagavatam 4.8; 1.5–6'),
('Prahlada','He holds to devotion while his father opposes it.','His prayer follows the appearance of Narasimha.','Bhagavatam 7.9'),
('Hiranyakashipu','He opposes the devotion of his own son.','He is Prahlada’s father.','Bhagavatam 7.5–9'),
('Narasimha','His appearance overturns a ruler’s confidence in his protections.','He is the man-lion form associated with Prahlada’s rescue.','Bhagavatam 7.8–9'),
('Gajendra','A long struggle in water leaves his ordinary strength insufficient.','He appeals for refuge while caught by a crocodile.','Bhagavatam 8.2–4'),
('Indra','A change in a village’s worship leads him to send destructive rain.','The Govardhana episode also becomes a lesson about pride.','Bhagavatam 10.24–27'),
('Yashoda','She tries to tie up a mischievous child, but the rope keeps falling short.','She is Krishna’s foster mother.','Bhagavatam 10.9'),
('Brahma','He tests a cowherd child and is surprised by what he discovers.','The missing calves and boys appear in the episode of his bewilderment.','Bhagavatam 10.13–14'),
('Kaliya','His presence makes part of a river dangerous.','Krishna confronts this serpent in the Yamuna.','Bhagavatam 10.16–17'),
('Bali','A small request becomes much larger than it first seems.','He receives Vamana’s request for three paces of land.','Bhagavatam 8.18–23'),
('Vamana','He comes to a generous king in a small form.','His request concerns three paces of land.','Bhagavatam 8.18–23'),
('Rantideva','His hospitality is tested when he has very little left.','He shares even the last water after a long fast.','Bhagavatam 9.21.2–18'),
('Prithu','He has to understand the cause of a food shortage before arranging a response.','The Earth speaks to him in the form of a cow.','Bhagavatam 4.17–18'),
('Akrura','His journey has both a political purpose and a devotional inner life.','He travels to bring Krishna and Balarama to Mathura.','Bhagavatam 10.38–40'),
('Sandipani','Two exceptional pupils learn under him and offer a teacher’s gift.','He teaches Krishna and Balarama.','Bhagavatam 10.45.30–50'),
('Markandeya','A vast flood becomes part of a vision that changes his sense of the world.','He sees a child resting on a banyan leaf.','Bhagavatam 12.8–10'),
('Shukadeva','His teaching is framed by a listener facing the end of life.','He teaches King Parikshit.','Bhagavatam 1.19'),
('Parikshit','He turns to hearing scripture when his remaining time is short.','Shukadeva answers his questions.','Bhagavatam 1.19'),
('Arjuna','He explains why a difficult responsibility feels unbearable.','Krishna is his charioteer in the Gita.','Bhagavad Gita 1.28–30'),
('Sanjaya','He reports a conversation rather than being its main student.','He speaks to Dhritarashtra.','Bhagavad Gita 1.1–2'),
('Dhritarashtra','His opening question asks what happened on the battlefield.','Sanjaya answers him.','Bhagavad Gita 1.1–2'),
('Krishna','He asks his student to reflect fully before choosing how to act.','He teaches Arjuna in the Gita.','Bhagavad Gita 18.63'),
('Rukmini','She takes part in a warm welcome for an unassuming visitor.','She attends during Krishna’s welcome of Sudama.','Bhagavatam 10.80'),
('Vasudeva','He carries a newborn away from the place of birth.','He is Krishna’s birth father.','Bhagavatam 10.3–5'),
('Devaki','Her child’s birth takes place under threat.','She is Krishna’s birth mother.','Bhagavatam 10.3'),
('Nanda','A child raised in his household becomes central to the cowherd stories.','He is Krishna’s foster father.','Bhagavatam 10.5'),
('Melpathur Narayana Bhattathiri','His devotional poem retells Bhagavata themes in short verse groups.','He composed Narayaneeyam, associated with Guruvayur.','Narayaneeyam · work introduction')]
DYNASTY=[
('Dhruva','father','Uttanapada','Bhagavatam 4.8'),('Dhruva','mother','Suniti','Bhagavatam 4.8'),('Uttama','father','Uttanapada','Bhagavatam 4.8'),('Uttama','mother','Suruchi','Bhagavatam 4.8'),
('Krishna','birth father','Vasudeva','Bhagavatam 10.3'),('Krishna','birth mother','Devaki','Bhagavatam 10.3'),('Krishna','foster father','Nanda','Bhagavatam 10.5'),('Krishna','foster mother','Yashoda','Bhagavatam 10.5; 10.9'),
('Prahlada','father','Hiranyakashipu','Bhagavatam 7.5'),('Prahlada','mother','Kayadhu','Bhagavatam 7.7'),('Kapila','mother','Devahuti','Bhagavatam 3.25'),('Kapila','father','Kardama','Bhagavatam 3.24'),
('Uttanapada','father','Svayambhuva Manu','Bhagavatam 4.1'),('Priyavrata','father','Svayambhuva Manu','Bhagavatam 4.1'),('Devahuti','father','Svayambhuva Manu','Bhagavatam 3.22'),('Bali','father','Virochana','Bhagavatam 8.19.13')]
SEQUENCES=[
('Sudama’s visit',['His wife encourages a visit','He carries a rice gift','Krishna welcomes him','They recall their school days','He returns home'],'Bhagavatam 10.80–81'),
('Dhruva’s search',['Dhruva feels hurt at home','He speaks to Suniti','Narada guides him','He follows a disciplined practice','He receives a divine vision'],'Bhagavatam 4.8–9'),
('Govardhana',['Krishna discusses the village observance','The villagers honour Govardhana','Indra sends heavy rain','Krishna shelters the community','Indra’s pride is addressed'],'Bhagavatam 10.24–27'),
('Gajendra',['The elephant enters the water','A crocodile seizes him','The struggle continues','His strength is insufficient','He calls for divine help'],'Bhagavatam 8.2–4'),
('Yashoda and the rope',['Krishna is involved in mischief','Yashoda tries to restrain him','The rope falls short','She keeps trying','Krishna allows himself to be bound'],'Bhagavatam 10.9'),
('Brahma’s bewilderment',['Brahma tests Krishna','The calves and boys are taken away','Krishna supplies their appearances','Brahma sees what defeats his expectations','He offers prayers'],'Bhagavatam 10.13–14'),
('Kaliya',['The river is made dangerous','Krishna enters the water','He confronts Kaliya','The serpent’s wives appeal','Kaliya leaves as directed'],'Bhagavatam 10.16–17'),
('Vamana and Bali',['Vamana approaches Bali','He asks for three paces','Bali grants the request','The small form becomes vast','Bali offers himself when the measure exceeds his land'],'Bhagavatam 8.18–23'),
('Prithu and the Earth',['A shortage troubles the people','Prithu confronts the Earth','The Earth explains the difficulty','A workable arrangement is made','Resources are drawn through that arrangement'],'Bhagavatam 4.17–18'),
('Akrura’s journey',['Akrura sets out for the cowherd settlement','He hopes to see Krishna','He meets Krishna and Balarama','The journey towards Mathura begins','He experiences a vision in the water'],'Bhagavatam 10.38–40'),
('Krishna’s education',['Krishna and Balarama study with Sandipani','They complete their learning','They ask what gift their teacher wants','They seek to restore his son','They return to their teacher'],'Bhagavatam 10.45.30–50'),
('The churning',['The groups prepare to churn','Mount Mandara serves as the churning rod','Vasuki serves as the rope','Dangerous poison emerges','The later gifts and nectar emerge'],'Bhagavatam 8.6–12'),
('The Gita’s conversation',['Dhritarashtra asks Sanjaya what happened','Arjuna surveys the armies','Arjuna describes his distress','Krishna teaches him','Arjuna says his confusion has cleared'],'Bhagavad Gita 1.1; 1.21–30; 2.7; 18.73')]
NAR_TOPICS=[
(1,'The nature and glory of the divine'),(2,'The beauty of the divine form and devotion'),(3,'A prayer for devotion and relief'),(4,'The practice of yoga'),(5,'The beginning of creation'),(6,'The cosmic form'),(7,'Brahma and creation'),(8,'Dissolution and a new cycle'),(9,'Brahma searches for his origin'),(10,'The variety of creation'),(11,'The sages and the Vaikuntha gatekeepers'),(12,'Varaha lifts the Earth'),(13,'Varaha defeats Hiranyaksha'),(14,'The birth and setting of Kapila'),(15,'Kapila’s teaching'),(16,'Nara and Narayana; Daksha’s sacrifice'),(17,'Dhruva’s devotion'),(18,'Prithu and the Earth'),(19,'The Prachetas'),(20,'Rishabha’s life'),(21,'The worlds and forms of worship'),(22,'Ajamila'),(23,'Daksha and Chitraketu'),(24,'Prahlada'),(25,'Narasimha'),(26,'Gajendra’s rescue')]
def bank():
 out=[]
 def add(book,prompt,options,answer,why,reference,hard=False):
  out.append({'book':book,'prompt':prompt,'choices':options,'answer':answer,'why':why,'reference':reference,'hard':hard,'id':book+':'+str(len(out))})
 for q in OLD:
  book='Gita' if 'Bhagavad Gita' in q['reference'] else 'Narayaneeyam' if q['reference'].startswith('Narayaneeyam') else 'Bhagavatam'
  add(book,q['prompt'],q['choices'],q['answer'],q['why'],q['reference'],q['level']=='Close readers')
 for i,(title,explanation,action,ref,situation) in enumerate(GITA):
  other=[GITA[(i+j)%18] for j in (3,7,11)]
  add('Gita',f'Which teaching best describes Gita {ref}?',[title]+[g[0] for g in other],0,explanation,'Bhagavad Gita '+ref)
  add('Gita',f'Which next step most directly reflects the teaching at Gita {ref}?',[action]+[g[2] for g in other],0,explanation+' This action is a modern application, not a literal quotation.','Bhagavad Gita '+ref,True)
  add('Gita',f'Which chapter contains the teaching used here: “{title}”?',[str(i+1)]+[str((i+j)%18+1) for j in (4,8,12)],0,explanation,'Bhagavad Gita '+ref,True)
 for i,(n,topic) in enumerate(NAR_TOPICS):
  others=[NAR_TOPICS[(i+j)%len(NAR_TOPICS)] for j in (3,7,11)]
  add('Narayaneeyam',f'Which subject belongs to Dasakam {n}?',[topic]+[t[1] for t in others],0,'This is the subject of this verse group. Read it in context rather than treating the title as a full explanation.',f'Narayaneeyam Dasakam {n}')
  add('Narayaneeyam',f'Which dasakam should you open to study {topic.lower()}?',[str(n)]+[str(t[0]) for t in others],0,'The matching verse group is Dasakam '+str(n)+'.',f'Narayaneeyam Dasakam {n}',True)
 for i,(name,clue,detail,ref) in enumerate(CHARACTERS):
  book='Gita' if ref.startswith('Bhagavad Gita') else 'Narayaneeyam' if ref.startswith('Narayaneeyam') else 'Bhagavatam'
  add(book,clue+' Who is this?',[name]+[CHARACTERS[(i+j)%len(CHARACTERS)][0] for j in (4,9,15)],0,detail,ref)
 for i,(child,relation,parent,ref) in enumerate(DYNASTY):
  alternatives=list(dict.fromkeys(x[2] for x in DYNASTY if x[2]!=parent))[:3]
  add('Bhagavatam',f'Who is {child}’s {relation}?',[parent]+alternatives,0,'Keep the relationship label: birth, upbringing and other family links are different.',ref,True)
 return out
QUIZ_BANK=bank()
