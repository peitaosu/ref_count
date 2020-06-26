using Microsoft.Win32;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ref_sharp
{
    class ReferenceManager
    {
        private string msi_key_string = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Installer\\UserData\\S-1-5-18\\Components\\";
        private string default_config = "ref.conf";

        public void LoadConfig()
        {
            
        }
        public bool Install()
        {
            return true;
        }
        public bool Uninstall()
        {
            return true;
        }
        public void AddReferences()
        {

        }
        public void ReduceReferences()
        {

        }
        private bool _add_count_in_registry(string component, string product, string file)
        {
            RegistryKey component_key = Registry.LocalMachine.OpenSubKey(msi_key_string + component, true);
            if (component_key == null)
            {
                component_key = Registry.LocalMachine.CreateSubKey(msi_key_string + component);
            }
            component_key.SetValue(product, file);
            component_key.Close();
            return true;
        }

        private bool _reduce_count_in_registry(string component, string product)
        {
            RegistryKey component_key = Registry.LocalMachine.OpenSubKey(msi_key_string + component, true);
            if (component_key.GetValue(product) != null)
                component_key.DeleteValue(product);
            component_key.Close();
            return true;
        }

        private int _get_count_in_registry(string component)
        {
            RegistryKey component_key = Registry.LocalMachine.OpenSubKey(msi_key_string + component, true);
            if(component_key != null)
                return component_key.ValueCount;
            return 0;
        }

        private bool _delete_count_in_registry(string component, string product)
        {
            RegistryKey component_key = Registry.LocalMachine.OpenSubKey(msi_key_string + component, true);
            if (component_key != null && component_key.GetValue(product) != null)
            {
                component_key.DeleteValue(product);
                component_key.Close();
            }
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
