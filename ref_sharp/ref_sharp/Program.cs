using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ref_sharp
{
    class ReferenceManager
    {
        public void LoadConfig()
        {
            
        }
        public bool Install() {
            return true;
        }
        public bool Uninstall()
        {
            return true;
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            ReferenceManager refman = new ReferenceManager();
            refman.LoadConfig();
            refman.Install();
            refman.Uninstall();
        }
    }
}
