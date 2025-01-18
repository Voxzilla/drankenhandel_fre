#import alle packages 
import pandas as pd


df_wave4 = pd.read_json('build/df_wave4_draaitabel')
# df_wave4 = pd.read_json('df_wave4')
#df_wave3 = pd.read_json('df_wave3_draaitabel')
# df_wave2 = pd.read_json('df_wave2')
# df_wave1 = pd.read_json('df_wave1')
#waves = [df_wave4, df_wave3, df_wave2, df_wave1]
#waves = [df_wave4, df_wave3]
#df_waves = pd.concat(df_wave4)
output_file = "build/draaitabel_wave4.xlsx"
df_wave4.to_excel(output_file, index=False, engine='xlsxwriter')
print(f"Excel toegevoegd in {output_file}")