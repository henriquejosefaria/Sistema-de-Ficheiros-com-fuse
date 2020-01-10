#!/usr/bin/env python

from __future__ import with_statement

import os
import sys
import errno
import random
import os.path
from shutil import copyfile

from fuse import FUSE, FuseOSError, Operations

from pymongo import MongoClient
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

cliente = MongoClient('mongodb://localhost:27017/')

dados = cliente['fuse']

class Passthrough(Operations):
    def __init__(self, root):
        # caminho do moutpoint
        self.root = root
        # variavel que indica que user esta autenticado
        self.autenticado = False
        # tempo em que foi requisitado o codigo
        self.tinicial = time.time()
    # Helpers
    # =======

    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path

    # Filesystem methods
    # ==================

    def access(self, path, mode):
        self.autenticado()
        if self.autenticado == True:
            full_path = self._full_path(path)
            if not os.access(full_path, mode):
                raise FuseOSError(errno.EACCES)
        else:
            pass

    def chmod(self, path, mode):
        self.autenticado()
        if self.autenticado == True:
            full_path = self._full_path(path)
            return os.chmod(full_path, mode)
        else:
            pass

    def chown(self, path, uid, gid):
        self.autenticado()
        if self.autenticado == True:
            full_path = self._full_path(path)
            return os.chown(full_path, uid, gid)
        else:
            pass

    def getattr(self, path, fh=None):
        self.autenticado()
        if self.autenticado == True:
            full_path = self._full_path(path)
            st = os.lstat(full_path)
            return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                        'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))
        else:
            pass

    def readdir(self, path, fh):
        self.autenticado()
        if self.autenticado == True:
            full_path = self._full_path(path)

            dirents = ['.', '..']
            if os.path.isdir(full_path):
                dirents.extend(os.listdir(full_path))
            for r in dirents:
                yield r
        else:
            pass

    def readlink(self, path):
        self.autenticado()
        if self.autenticado == True:
            pathname = os.readlink(self._full_path(path))
            if pathname.startswith("/"):
                # Path name is absolute, sanitize it.
                return os.path.relpath(pathname, self.root)
            else:
                return pathname
        else:
            pass

    def mknod(self, path, mode, dev):
        self.autenticado()
        if self.autenticado == True:
            return os.mknod(self._full_path(path), mode, dev)
        else:
            pass

    def rmdir(self, path):
        self.autenticado()
        if self.autenticado == True:
            full_path = self._full_path(path)
            return os.rmdir(full_path)
        else:
            pass

    def mkdir(self, path, mode):
        self.autenticado()
        if self.autenticado == True:
            return os.mkdir(self._full_path(path), mode)
        else:
            pass

    def statfs(self, path):
        self.autenticado()
        if self.autenticado == True:
            full_path = self._full_path(path)
            stv = os.statvfs(full_path)
            return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
                'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
                'f_frsize', 'f_namemax'))
        else:
            pass

    def unlink(self, path):
        self.autenticado()
        if self.autenticado == True:
            return os.unlink(self._full_path(path))
        else:
            pass

    def symlink(self, name, target):
        self.autenticado()
        if self.autenticado == True:
            return os.symlink(target, self._full_path(name))
        else:
            pass

    def rename(self, old, new):
        self.autenticado()
        if self.autenticado == True:
            return os.rename(self._full_path(old), self._full_path(new))
        else:
            pass

    def link(self, target, name):
        self.autenticado()
        if self.autenticado == True:
            return os.link(self._full_path(name), self._full_path(target))
        else:
            pass

    def utimens(self, path, times=None):
        self.autenticado()
        if self.autenticado == True:
            return os.utime(self._full_path(path), times)
        else:
            pass
    # File methods
    # ============

    def open(self, path, flags):
        self.autenticado()
        if self.aut==True:
            full_path = self._full_path(path)
            return os.open(full_path, flags)
        else:
            pass

    def create(self, path, mode, fi=None):
        self.autenticado()
        if self.autenticado == True:
            full_path = self._full_path(path)
            return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)
        else:
            pass

    def read(self, path, length, offset, fh):
        self.autenticado()
        if self.autenticado == True:
            os.lseek(fh, offset, os.SEEK_SET)
            return os.read(fh, length)
        else:
            pass

    def write(self, path, buf, offset, fh):
        self.autenticado()
        e = entropia(buf)
        if self.autenticado == True and e:
            if not os.path.isdir("safe"):
                mkdir("safe",0600)
            shutil.copy(os.path.join(path,fh), os.path.join(path,'dir/'+fh))
            f=os.popen('id -nu','r')
            uid=f.read()
            uid=uid.strip()
            mongo.db.ransomware.insert({"userId": uid, "time": timestamp})
            os.lseek(fh, offset, os.SEEK_SET)
            return os.write(fh, buf)
        elif self.autenticado == True:
            os.lseek(fh, offset, os.SEEK_SET)
            return os.write(fh, buf)
        else:
            pass

    def truncate(self, path, length, fh=None):
        self.autenticado()
        if self.autenticado == True:
            full_path = self._full_path(path)
            with open(full_path, 'r+') as f:
                f.truncate(length)
        else:
            pass

    def flush(self, path, fh):
        self.autenticado()
        if self.autenticado == True:
            return os.fsync(fh)
        else:
            pass

    def release(self, path, fh):
        self.autenticado()
        if self.autenticado == True:
            return os.close(fh)
        else:
            pass

    def fsync(self, path, fdatasync, fh):
        self.autenticado()
        if self.autenticado == True:
            return self.flush(path, fh)
        else:
            pass

    def autenticado(self):
        timedif = time.time() - self.tinicial
        # user tem 2 mnutos de acesso
        if self.autenticado == True and timedif <= 120:
            pass
        else:
            self.autenticado = False
            f=os.popen('id -nu','r')
            uid=f.read()
            uid=uid.strip()
            a = validUser(uid)
            if a == True:
                self.autenticado = True
                self.tinicial=time.time()
            else:
                self.aut = False

    def validUser(uid):
        f = os.popen('id -nu', 'r')
        uid = f.read()
        f.close()
        uid = uid.strip()
        if mongo.db.log.find({"userId": uid, "time": self.tinicial, "acess": "valid"}).count() > 0:
            mongo.db.log.update({"userId": uid, "time": self.tinicial, "acess": "valid"},{"userId": uid, "time": self.tinicial, "acess": "invalid"})
        msg = MIMEMultipart()
        code = str(random.randint(100000,1000000))
        message = "Thank you  for using our services !!\n\n Requested code: "+ code
        password = "workaholics2020"
        msg['From'] = "workaholicsTS2020@gmail.com"
        msg['To'] = file["email"]
        msg['Subject'] = "Requested code"
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        #create server
        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        # Login Credentials for sending the mail
        server.login(msg['From'], password)
        # send the message via the server.
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        mongo.db.validCodes.insert({"userId": uid , "code": code})
        time = time.time()
        while time.time()-time <= 60:
            if mongo.db.log.find({"userId": uid, "acess": "valid"}).count() > 0:
                return render_template("verify.html", title="verify",time = time.time())
                return True
            else: 
                time.sleep(2)
        return False

    def entropia(buf):
        ocorrencias = {}
        for c in buf:
            if c in ocorrencias:
                ocorrencias[c] = ocorrencias[c] + 1
            else:
                ocorrencias[c] = 1
        prob = []
        length = len(buf)
        # calcula probabilidade de cada elemento distinto
        for c in ocorrencias:
            prob.append(c/length)
            length2 = len(ocorrencias)
            randomelements = 0
        # Caso 92% dos elementos ou mais tenham uma distribuicao entre  48% e 52% assume-se que e um elemento usado para cifrar
        for p in prob:
            if b > 0.48  and b < 0.52:
                randomelements += 1
        if randomelements/length2 > 0.92:
            return True
        return False



def main(mountpoint, root):
    FUSE(Passthrough(root), mountpoint, nothreads=True, foreground=True)

if __name__ == '__main__':
    main(sys.argv[2], sys.argv[1])