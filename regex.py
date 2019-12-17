from re import compile

GREETING = compile(r"^((h+e+ll+o+)|(gr+ee+ti+n+gs+)|(hi+)|(h+e+y+)|(((wa)|')?s+u+p+)|(y+o+)|(szia))\b")
BOT_MENTION = compile(r'\b((bot)|(gqbot)|(lilgq))\b')
FAREWELL = compile(r"^(((c|(see)) ?y((a+)|(ou)))|((goo+d)?(by+e+))|" +
                   "((g((ood)?)(.?))?n+(i((te)|(ght)))?)|(おやすみ(なさい)?)|(farewell))\b")
NIGHT = compile(r"^(((g((ood)?)(.?))?n+(i((te)|(ght)))?)|(おやすみ(なさい)?))\b")
