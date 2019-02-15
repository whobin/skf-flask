import unittest, sys, time, skf
from skf import settings
from skf.db_tools import init_db, connect_db
from skf.app import app
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

class SKFClickThrough(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.client = app.test_client()
        with app.app_context():
            init_db(True)
            settings.TESTING = True
        self.driver = webdriver.Chrome()
        driver = self.driver
        driver.get("http://localhost:4200")
        username = driver.find_element_by_name("username")
        password = driver.find_element_by_name("password")
        username.send_keys("admin")
        password.send_keys("admin")
        password.send_keys(Keys.RETURN)


    """
    ////////////////////////////////////////////////////////////////////////////////////
    Test the dashboard icon links
    ////////////////////////////////////////////////////////////////////////////////////
    """
    
    def test_a_dashboard_icon_link_to_checklist(self):
        """Test Dashboard Icon button to checklist"""
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        input = wait.until(EC.visibility_of_element_located((By.ID, "checklist-icon")))
        input.click()
        assert "Security checklists" in driver.page_source


    def test_b_dashboard_icon_link_to_project_list(self):
        """Test Dashboard Icon button to projects"""
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        input = wait.until(EC.visibility_of_element_located((By.ID, "project-list-icon")))
        input.click()
        assert "All projects" in driver.page_source


    def test_c_dashboard_icon_link_to_code_example(self):
        """Test Dashboard Icon button to code examples"""
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        input = wait.until(EC.visibility_of_element_located((By.ID, "code-examples-icon")))
        input.click()
        assert "Code examples" in driver.page_source


    def test_d_dashboard_icon_link_to_knowledge_base(self):
        """Test Dashboard Icon button to knowledge base items"""
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        input = wait.until(EC.visibility_of_element_located((By.ID, "knowledgebase-icon")))
        input.click()
        assert "Knowledge Base" in driver.page_source


    """
    ////////////////////////////////////////////////////////////////////////////////////
    Test creating/deleting a checklist
    ////////////////////////////////////////////////////////////////////////////////////
    """

    def test_e_checklist_new_checklist_flow(self):
        """Test manage checklist ad new checklist"""
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        input = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Checklist options")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "checklist-summary")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "add-new-checklist")))
        input.click()
        checklistType = driver.find_element_by_name("checklistType")
        checklistDescription = driver.find_element_by_name("checklistDescription")
        checklistType.send_keys("selenium-stored-checklist")
        checklistDescription.send_keys("selenium-stored-checklist")
        input = wait.until(EC.visibility_of_element_located((By.ID, "store-checklist")))
        input.click()
        time.sleep(2)
        assert "selenium-stored-checklist" in driver.page_source
    

    def test_f_checklist_delete_checklist_flow(self):
        """Test manage checklist delete item"""
        driver = self.driver
        wait = WebDriverWait(driver, 10)     
        input = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Checklist options")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "checklist-summary")))
        input.click()
        input = wait.until(EC.element_to_be_clickable((By.ID, 'delete-checklist1')))
        input.click()
        time.sleep(2)        
        delete = driver.find_element_by_name("delete")
        delete.send_keys("DELETE")
        input = wait.until(EC.visibility_of_element_located((By.ID, "delete-checklist-finalized")))
        input.click()
        time.sleep(2)
        assert "filled-checklist-for-testing" not in driver.page_source

    """
    ////////////////////////////////////////////////////////////////////////////////////
    Test creating/deleting/updating checklist items
    ////////////////////////////////////////////////////////////////////////////////////
    """


    def test_g_test_back_button_create_checklist_items(self):
        """Test manage checklist create new item's back button"""
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        input = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Checklist options")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "checklist-summary")))
        input.click()
        input = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "empty-checklist-for-testing")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "checklist-add-new-icon")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "back-button")))
        input.click()
        time.sleep(2)
        assert "Manage your checklists!" in driver.page_source


    def test_h_create_new_checklist_item_flow(self):
        """Test manage checklist create new checklist item"""
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        input = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Checklist options")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "checklist-summary")))
        input.click()
        input = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "empty-checklist-for-testing")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "checklist-add-new-icon")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "add-new-checklist-item")))
        input.click()
        wait.until(EC.visibility_of_element_located((By.ID, "insert-new-checklist-item")))
        checklistID = driver.find_element_by_name("checklistID")
        checklistID.send_keys("1.1")
        content = driver.find_element_by_name("content")
        content.send_keys("Control content")       
        input = wait.until(EC.visibility_of_element_located((By.ID, "select-knowledge-base-item")))
        input.click()
        time.sleep(1)
        input = driver.find_element_by_xpath("//*[contains(text(),'#1')]")
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "select-question-pre-id")))
        input.click()
        time.sleep(1)
        input = driver.find_element_by_xpath("//*[contains(text(),'test-question-pre')]")
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "select-question-sprint-id")))
        input.click()
        time.sleep(1)
        input = driver.find_element_by_xpath("//*[contains(text(),'test-question-sprint')]")
        input.click()
        select = Select(driver.find_element_by_id('select-include-first'))
        select.select_by_visible_text('true')
        select = Select(driver.find_element_by_id('select-include-always'))
        select.select_by_visible_text('true')
        input = wait.until(EC.visibility_of_element_located((By.ID, "insert-new-checklist-item")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Checklist options")))
        time.sleep(2)
        assert "Control content" in driver.page_source
    
    def test_i_update__checklist_item_flow(self):
        """Test manage checklist update checklist item"""
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        input = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Checklist options")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "checklist-summary")))
        input.click()
        input = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "filled-checklist-for-testing")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "checklist-add-new-icon")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "1.1")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "edit-checklist-item-content")))
        input.click()
        time.sleep(5)
        content = driver.find_element_by_name("content")
        content.clear()
        content.send_keys("Updated control content")
        input = wait.until(EC.visibility_of_element_located((By.ID, "update-checklist-control")))
        input.click()
        time.sleep(2)
        assert "Updated control content" in driver.page_source
    


    def test_j_delete__checklist_item_flow(self):
        """Test manage checklist delete checklist item"""
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        input = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Checklist options")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "checklist-summary")))
        input.click()
        input = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "filled-checklist-for-testing")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "checklist-add-new-icon")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "1.1")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "edit-checklist-item-content")))
        input.click()
        time.sleep(3)
        input = wait.until(EC.visibility_of_element_located((By.ID, "show-delete-modal")))
        input.click()
        delete = driver.find_element_by_name("delete")
        delete.send_keys("DELETE")
        input = wait.until(EC.visibility_of_element_located((By.ID, "delete-checklist-item-finalized")))
        input.click()
        time.sleep(2)
        assert "Updated control content" not in driver.page_source
      
    """
    ////////////////////////////////////////////////////////////////////////////////////
    Test creating/deleting/updating pre-development questions
    ////////////////////////////////////////////////////////////////////////////////////
    """


    def test_k_add__pre_question_flow(self):
        """Test manage checklist add new pre question"""
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        input = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Checklist options")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "checklist-summary")))
        input.click()
        input = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "empty-checklist-for-testing")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "questionnaire-pre-icon")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "add-question-modal")))
        input.click()
        content = driver.find_element_by_name("questionName")
        content.send_keys("selenium-added-question")
        input = wait.until(EC.visibility_of_element_located((By.ID, "add-new-question")))
        input.click()
        time.sleep(2)
        Select(driver.find_element_by_id('select-question'))
        time.sleep(2)
        assert "selenium-added-question" in driver.page_source
    

    def test_l_update__pre_question_flow(self):
        """Test manage checklist update pre question"""
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        input = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Checklist options")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "checklist-summary")))
        input.click()
        input = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "filled-checklist-for-testing")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "questionnaire-pre-icon")))
        input.click()
        time.sleep(2)
        select = Select(driver.find_element_by_id('select-question'))
        select.select_by_visible_text('test-question-pre')
        input = wait.until(EC.visibility_of_element_located((By.ID, "update-question-modal")))
        input.click()
        content = driver.find_element_by_name("questionName")
        content.send_keys("selenium-updated-question")
        input = wait.until(EC.visibility_of_element_located((By.ID, "update-question")))
        input.click()
        time.sleep(2)
        Select(driver.find_element_by_id('select-question'))
        time.sleep(2)
        assert "selenium-updated-question" in driver.page_source
    

    def test_m_delete__pre_question_flow(self):
        """Test manage checklist delete pre question"""
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        input = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Checklist options")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "checklist-summary")))
        input.click()
        input = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "filled-checklist-for-testing")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "questionnaire-pre-icon")))
        input.click()
        time.sleep(2)
        select = Select(driver.find_element_by_id('select-question'))
        time.sleep(2)
        select.select_by_visible_text('test-question-pre')
        input = wait.until(EC.visibility_of_element_located((By.ID, "delete-question-modal")))
        input.click()
        time.sleep(2)
        content = driver.find_element_by_name("delete")
        content.send_keys("DELETE")
        input = wait.until(EC.visibility_of_element_located((By.ID, "delete-question")))
        input.click()
        time.sleep(2)
        assert "test-question-pre" not in driver.page_source  


    """
    ////////////////////////////////////////////////////////////////////////////////////
    Test correlating controls to pre-development questions
    ////////////////////////////////////////////////////////////////////////////////////
    """


    def test_n_correlate__pre_question_flow(self):
        """Test manage checklist correlate pre question"""
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        input = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Checklist options")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "checklist-summary")))
        input.click()
        input = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "filled-checklist-for-testing")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "questionnaire-pre-icon")))
        input.click()
        time.sleep(2)
        select = Select(driver.find_element_by_id('select-question'))
        select.select_by_visible_text('test-question-pre')
        time.sleep(2)
        input = driver.find_element_by_xpath("//*[contains(text(), '1.1')]")
        input.click()
        time.sleep(2)
        compare = wait.until(EC.visibility_of_element_located((By.ID, "checklist-correlated0"))).text
        assert "1.1" in compare


    def test_o_test__pre_question_back_button(self):
        """Test manage checklist pre question back button"""
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        input = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Checklist options")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "checklist-summary")))
        input.click()
        input = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "empty-checklist-for-testing")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "questionnaire-pre-icon")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "back-button")))
        input.click()
        time.sleep(2)
        assert "Manage your checklists!" in driver.page_source

    """
    ////////////////////////////////////////////////////////////////////////////////////
    Test creating/deleting/updating post-development questions
    ////////////////////////////////////////////////////////////////////////////////////
    """


    def test_p_add__sprint_question_flow(self):
        """Test manage checklist add new sprint question"""
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        input = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Checklist options")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "checklist-summary")))
        input.click()
        input = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "empty-checklist-for-testing")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "questionnaire-sprint-icon")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "add-question-modal")))
        input.click()
        content = driver.find_element_by_name("questionName")
        content.send_keys("selenium-added-question")
        input = wait.until(EC.visibility_of_element_located((By.ID, "add-new-question")))
        input.click()
        time.sleep(2)
        Select(driver.find_element_by_id('select-question'))
        time.sleep(2)
        assert "selenium-added-question" in driver.page_source


    def test_q_update__sprint_question_flow(self):
        """Test manage checklist update sprint question"""
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        input = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Checklist options")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "checklist-summary")))
        input.click()
        input = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "filled-checklist-for-testing")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "questionnaire-sprint-icon")))
        input.click()
        time.sleep(2)
        select = Select(driver.find_element_by_id('select-question'))
        select.select_by_visible_text('test-question-sprint')
        input = wait.until(EC.visibility_of_element_located((By.ID, "update-question-modal")))
        input.click()
        content = driver.find_element_by_name("questionName")
        content.send_keys("selenium-updated-question")
        input = wait.until(EC.visibility_of_element_located((By.ID, "update-question")))
        input.click()
        time.sleep(2)
        Select(driver.find_element_by_id('select-question'))
        time.sleep(2)
        assert "selenium-updated-question" in driver.page_source


    def test_r_delete__sprint_question_flow(self):
        """Test manage checklist delete sprint question"""
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        input = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Checklist options")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "checklist-summary")))
        input.click()
        input = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "empty-checklist-for-testing")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "questionnaire-sprint-icon")))
        input.click()
        time.sleep(2)
        select = Select(driver.find_element_by_id('select-question'))
        select.select_by_visible_text('test-question-sprint')
        input = wait.until(EC.visibility_of_element_located((By.ID, "delete-question-modal")))
        input.click()
        time.sleep(2)
        content = driver.find_element_by_name("delete")
        content.send_keys("DELETE")
        input = wait.until(EC.visibility_of_element_located((By.ID, "delete-question")))
        input.click()
        time.sleep(2)
        assert "test-question-sprint" not in driver.page_source  

    
    """
    ////////////////////////////////////////////////////////////////////////////////////
    Test correlating controls to post-development questions
    ////////////////////////////////////////////////////////////////////////////////////
    """   


    def test_s_correlate__sprint_question_flow(self):
        """Test manage checklist correlate sprint question"""
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        input = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Checklist options")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "checklist-summary")))
        input.click()
        input = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "filled-checklist-for-testing")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "questionnaire-sprint-icon")))
        input.click()
        time.sleep(2)
        select = Select(driver.find_element_by_id('select-question'))
        select.select_by_visible_text('test-question-sprint')
        time.sleep(2)
        input = driver.find_element_by_xpath("//*[contains(text(), '1.1')]")
        input.click()
        time.sleep(2)
        compare = wait.until(EC.visibility_of_element_located((By.ID, "checklist-correlated0"))).text
        assert "1.1" in compare


    def test_t_test__sprint_question_back_button(self):
        """Test manage checklist sprint question back button"""
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        input = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Checklist options")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "checklist-summary")))
        input.click()
        input = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "empty-checklist-for-testing")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "questionnaire-sprint-icon")))
        input.click()
        input = wait.until(EC.visibility_of_element_located((By.ID, "back-button")))
        input.click()
        time.sleep(2)
        assert "Manage your checklists!" in driver.page_source
    

    @classmethod
    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()

    
