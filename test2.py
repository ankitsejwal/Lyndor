import chapters


lynda_folder_path = "/Volumes/750 GB/Movies/Lynda-collection/"
urlink = "https://www.lynda.com/Dreamweaver-tutorials/Dreamweaver-CS6-Essential-Training/97613-2.html?srchtrk=index%3a3%0alinktypeid%3a2%0aq%3adreamweaver+essentials%0apage%3a1%0as%3arelevance%0asa%3atrue%0aproducttypeid%3a2"
   
chapters.save_chapters(urlink, lynda_folder_path)
