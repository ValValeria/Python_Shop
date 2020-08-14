
     
class Perm():
      def can(self,action,user,obj):
         self._user=user
         self._obj=obj 
         self._action=action
         return self.decide()
        
      def decide(self):
         if '_all' in self._action:
             ability=getattr(self._user.role,self._action.strip(),None) #если всех прав нет 
             if not ability:
                    return getattr(self,self._action,None)
             return True 
         else:
             return getattr(self,self._action,None)

                   
      @property
      def update(self):
          ability=self._user.role.can_update_all
          if not ability:
              return self._user.id==self._post.user_id
          else:
              return True  

      @property
      def create_post(self):
          return True

      @property
      def delete_users(self):
          return getattr(self._user.role,'show_profile_all',None)

      @property
      def add_users(self):
          return getattr(self._user.role,'show_profile_all',None)
      
      @property
      def delete(self):
          return self._user.id==self._obj.id

      def __str__(self):
          return 
