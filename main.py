from tkinter import *
from tkinter import filedialog as fd
import os

fields = ('Chemin', 'Heure début', 'Date', 'Fps', 'Dossier de sortie')

chemin_field = None

def makeform(root, fields):
   global chemin_field
   entries = {}
   for field in fields:
      row = Frame(root)
      lab = Label(row, width=13, text=field+": ", anchor='w')
      ent = Entry(row)
      if field == fields[0]:
          chemin_field = ent
      row.pack(side = TOP, fill = X, padx = 5 , pady = 5)
      lab.pack(side = LEFT)
      ent.pack(side = RIGHT, expand = YES, fill = X)
      entries[field] = ent
   return entries
   
def add_date_time(entries):
   video_in = entries['Chemin'].get()
   video_ext = ('.mp4', '.mov')
   timecode = entries['Heure début'].get().replace(':', '\:')
   video_date = entries['Date'].get()
   framerate = entries['Fps'].get()
   out_dir = entries['Dossier de sortie'].get()
   
   if not os.path.isfile(video_in):
       video_in = entries['Chemin'].get()
       print(f"{video_in} not valid")
   
   if not out_dir or not os.path.isdir(out_dir):
       out_dir = os.path.join(os.path.dirname(video_in), "output")
       os.makedirs(out_dir, exist_ok=True)
   
   video_out = os.path.join(out_dir, os.path.basename(video_in))
   
   command = "ffmpeg -i \"{input}\" -vf \"drawtext=timecode='{tc}':r={fps}:x=(w-tw)/2:y=h-(lh):fontsize=50: text={take_date}: box=1:boxcolor=black@0.8:fontcolor=white\" -c:a copy \"{output}\"".format(input=video_in, output=video_out, tc=timecode, fps=framerate, take_date=video_date + '-')
            
   print(command) # debugging only
   
   os.system(command)
   
   os.startfile(out_dir)
   
def select_file():
   filetypes = (
	   ('Video files', '*.mp4;*.flv;*.avi;*.mkv'),
	   ('All files', '*.*')
   )

   filename = fd.askopenfilename(title='Selectionner une vidéo', initialdir='/', filetypes=filetypes)
   
   if chemin_field:
	   chemin_field.insert(0, filename)


if __name__ == '__main__':
   root = Tk()
   root.title('Timestamper')
   ents = makeform(root, fields)
   root.bind('<Return>', (lambda event, e = ents: fetch(e)))
   b_chemin = Button(root, text = 'Choisir un fichier', command=select_file)
   b_chemin.pack(side = LEFT, padx = 5, pady = 5)
   b1 = Button(root, text = 'Démarrer',
      command=(lambda e = ents: add_date_time(e)))
   b1.pack(side = LEFT, padx = 5, pady = 5)
   b2 = Button(root, text = 'Quitter', command = root.quit)
   b2.pack(side = LEFT, padx = 5, pady = 5)
   root.mainloop()
