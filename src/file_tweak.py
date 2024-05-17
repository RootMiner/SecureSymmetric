# need to <<fix>> this, user is not allowed to change file name
def file_tweak(file_name, path, is_enc=None):
  if is_enc:
    mod_file_name = 'enc_' + file_name
    if path != file_name: 
      file_path = path + mod_file_name
    else: file_path = mod_file_name
  elif is_enc is None:
    if 'enc_' in file_name: 
      mod_file_name = file_name[4:]
    else: mod_file_name = file_name
    if path != file_name: 
      file_path = path + mod_file_name
    else: file_path = mod_file_name
  return file_path, mod_file_name

if __name__ == '__main__': file_tweak()