import re
from konlpy.tag import Twitter; t = Twitter()

class hangul_util():
	 
    def get_clean_hangul(self,tweet):
        try:
            hangul = re.findall(u'[\uAC00-\uD7A3]+', tweet)
            join_hangul = ' '.join(hangul)

            if(len(join_hangul) <= 0):
                return join_hangul

            hangul = t.morphs(join_hangul)

        except Exception as e:
            print('hangul except')
            if hasattr(e,'message'):
                print(e.message)
            else:
                print(e)

            pass

        return hangul
