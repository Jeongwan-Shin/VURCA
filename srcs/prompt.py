# prompt version : ver1
ver_qry_from_reason_ver1="""After checking your reasoning, questions, and answers, please create questions to clarify and double-check your answers.

Reasoning:The video describes the girl interacting with the electric toothbrush, pressing its buttons, and holding it up to her face. Among the options provided, "turning it around repeatedly" aligns with her actions and reflects excitement through playful interaction with the toy.
Question:how does the girl show her excitment over the toy?
Answer:By turning it around repeatedly
Please create a question to clarify the answer to that question.
verification:
- Did the girl show her excitement over the toy by turning it around repeatedly?
- Was turning the toy around repeatedly the main way the girl expressed her excitement?
- Did the girl perform any actions other than turning the toy around to show her excitement?

Reasoning:The description mentions children playing on swings, but no specific reference is made to a girl in blue or a headset, paws, or holding a baby. The action of moving a swing is typically done by either pushing someone or using feet to generate momentum. Since the swing motion is likely self-driven, "running her feet on the ground" fits best as the described method.
Question:how did the girl in blue moved the swing?
Answer:Running her feet on ground
Please create a question to clarify the answer to that question.
verification:
- Did the girl in blue move the swing by running her feet on the ground?
- Was the swing's motion entirely self-driven by the girl in blue?
- Did the girl in blue use any other method besides running her feet on the ground to move the swing?

Reasoning:The dog is described as mostly lying still with minimal movement. Among the actions, "putting a paw on the floor" is the most natural and plausible choice.
Question:what does the dog do after lying still for a while in the middle?
Answer:put hand on floor
Please create a question to clarify the answer to that question.
verification:
- Does the dog put its paw on the floor after lying still for a while?
- Is putting its paw on the floor a common behavior for the dog when it lies still?
- Did the dog remain completely still before putting its paw on the floor?

Reasoning:%s
Question:%s
Please create a question to clarify the answer to that question.
verification:
"""

atomic_question_ver2="""After reviewing the questions and answers, generate atomic questions to clarify and verify your responses.

Question:how does the girl show her excitment over the toy?
Answer:By turning it around repeatedly
Atomic Questions:
-Is the girl excited about the toy?
-Does the girl turn the toy around repeatedly?
-Is the girl's excitement shown through her actions?
-Is the toy the source of the girl's excitement?
-Does the girl's action indicate excitement?

Question:what does the dog do after lying still for a while in the middle?
Answer:put hand on floor
Atomic Questions:
-Does the dog lie still in the middle?
-Does the dog move after lying still for a while?
-Does the dog put its hand on the floor?
-Is the floor where the dog places its hand?
-Does the dog's action happen after lying still for a while?

Question:what does the dog do after lying still for a while in the middle?
Answer:put hand on floor
Atomic Questions:
-Does the dog lie still for a while?
-Is the dog in the middle while lying still?
-Does the dog move after lying still for a while?
-Does the dog put its hand on the floor?
-Is the action of putting the hand on the floor done after lying still?

Question:%s
Atomic Questions:
"""

atomic_question_ver3="""After reviewing the questions and answers, generate atomic questions to clarify and verify your responses, ensuring that the questions can be answered with a simple 'yes' or 'no'.

Question:how does the girl show her excitment over the toy?
Answer:By turning it around repeatedly
Atomic Questions:
-Can it be said that the girl is excited about the toy, as shown by her turning it around repeatedly? 
-Is the girl turning the toy around repeatedly to show her excitement?
-Can the girl's excitement be inferred from her action of turning the toy around repeatedly?
-Is the toy the reason for the girl's excitement, as evidenced by her turning it around repeatedly?
-Does the girl's action of turning the toy around repeatedly suggest she is excited?

Question:what does the dog do after lying still for a while in the middle?
Answer:put hand on floor
Atomic Questions:
-Can it be said that the dog lies still in the middle before putting its hand on the floor?
-Does the dog move by putting its hand on the floor after lying still for a while?
-Is the dog's action of putting its hand on the floor observed?
-Does the dog place its hand specifically on the floor?
-Does the dog put its hand on the floor after lying still for a while?

Question:what does the dog do after lying still for a while in the middle?
Answer:put hand on floor
Atomic Questions:
-Can it be said that the dog lies still for a while before putting its hand on the floor?
-Is the dog in the middle of the area while lying still before putting its hand on the floor?
-Does the dog move by putting its hand on the floor after lying still for a while?
-Is the dog's action of putting its hand on the floor observed?
-Does the dog put its hand on the floor specifically after lying still for a while?

Question:%s
Atomic Questions:
"""